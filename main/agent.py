import openai
import google.generativeai as genai
import logging
from retry import retry
from consts import *
from parse import *
from utils import cal_token, read_json
from prompt import Prompt
import sys
import requests

class DeepInfraClient():
    def __init__(self, api_key: str, base_url: str):
        self.url = base_url
        self.headers = {"Authorization": "bearer {}".format(api_key)}
    
    def call(self, query):
        return requests.post(self.url, headers=self.headers, json={"input": query}).json()

class Agent():
    def __init__(self, model_name, role="localizer", lang="C", temperature=0.9) -> None:
        self.model_name = model_name
        self.role = role
        self.lang = lang
        self.temperature = temperature
        self.client = self.__set_client()
        self.sys_msg = [{"role": "system", "content": get_sys_prompt(self.role, self.lang)}]
    
    def __print_msgs(self, msgs):
        token_num = cal_token(msgs)
        print("API calling...token number", token_num, "\n", "^"*40)
        # for lst in msgs:
        #     if lst["content"].startswith("Faulty"):
        #         print(lst["content"])
        #     print("#", len(lst["content"])//2, lst["content"].split('\n')[0].split('.')[0])
        # print("^"*30)
        return token_num
    
    def __set_client(self):
        config = read_json("./config.json")
        if self.model_name.startswith("gpt"):
            return openai.OpenAI(
                api_key=config["ChatGPT"]
            )
        
        if self.model_name.startswith("deepseek"):
            return openai.OpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=config["DeepSeek"]
            )

        if self.model_name.startswith("gemini"):
            genai.configure(api_key=config["Gemini"])
            safety_settings_NONE=[
                { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
                { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
                { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
                { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            return genai.GenerativeModel('gemini-pro',
                                         safety_settings=safety_settings_NONE,
                                         generation_config=genai.GenerationConfig(temperature=self.temperature)).start_chat(history=[])
        
        if self.model_name.endswith("starcoder"):
            return DeepInfraClient(
                base_url="https://api.deepinfra.com/v1/inference/bigcode/starcoder",
                api_key=config["DeepInfra"]
            )
        
        for m in ["codellama", "gemma"]:
            if m in self.model_name.lower():
                return openai.OpenAI(
                    base_url="https://api.deepinfra.com/v1/openai",
                    api_key=config["DeepInfra"]
                )
    
    def msgs2text(self, msgs):
        multi_turn = False
        for i in range(1, len(msgs)+1):
            if msgs[len(msgs)-i]["role"] == "assistant":
                multi_turn = True
                start_idx = len(msgs)-i + 1
                break
        if not multi_turn:
            return "\n".join([v["content"] for v in msgs])
        else:
            return "\n".join([v["content"] for v in msgs[start_idx:]])

    @retry((openai.APIConnectionError, openai.APIError, openai.Timeout), delay=2, backoff=2)
    def __launch_chatgpt(self, msgs, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name, 
                messages=msgs,
                temperature=temperature,
                #seed=42
            )
        except openai.BadRequestError:
            logging.warning("openai.BadRequestError: Error code: 400 - {'detail': 'Content Exists Risk'}")
            return None
        status_code = response.choices[0].finish_reason
        logging.info("GPT: "+response.choices[0].message.content)
        print("="*50)
        if status_code == "stop":
            return response.choices[0].message.content
        elif status_code == "length":
            logging.warning(f"The response is too long {len(response.choices[0].message.content)}")
            return response.choices[0].message.content
        elif status_code == "content_filter":
            logging.warning("Input contains risky contents!")
            return None
        else:
            logging.warning(response.choices[0].message.content)
            raise ValueError(f"The status code was {status_code}.")

    @retry((genai.types.generation_types.StopCandidateException, genai.types.generation_types.BlockedPromptException), delay=2, backoff=2)
    def __launch_gemini(self, msgs_text):
        response = self.client.send_message(msgs_text)
        status_code = response.candidates[0].finish_reason._name_
        if status_code == "STOP":
            return response.text
        else:
            logging.warning(response.text)
            raise ValueError(f"The status code was {status_code}.")

    def __launch_deepctl(self, msgs_test):
        response = self.client.call(msgs_test)
        status_code = response["inference_status"]["status"]
        if status_code == "succeeded":
            return response["results"][0]["generated_text"]
        else:
            logging.warning(response["results"][0]["generated_text"])
            raise ValueError(f"The status code was {status_code}.")

    @retry((ParseError), delay=2, backoff=2)
    def launch(self, msgs, temperature=0.7):
        token_num = self.__print_msgs(msgs)
        if token_num  < token_limit[self.model_name]:
            if self.model_name.startswith("gemini"):
                response_text = self.__launch_gemini(self.msgs2text(msgs))
            elif self.model_name.endswith("starcoder"):
                response_text = self.__launch_deepctl(self.msgs2text(msgs))
            else:
                response_text = self.__launch_chatgpt(msgs, temperature)
            return response_text
        else:
            logging.error("The prompt is too long")
            return None
             
    def run(self, prompt_obj: Prompt, extra_msgs=[], count_limit=3, temperature=0.7):
        role_msgs = [
            {"role": "user", "content": "Problem Description:\n"+prompt_obj.description.replace("balls", "boxes")},
            {"role": "user", "content": "Example:\n"+prompt_obj.example}]
        if self.role != "developer":
            role_msgs += [{"role": "user", "content": f"Faulty Code:\n"+prompt_obj.program}]
        role_prompt = get_role_prompt(self.role, self.lang)
        
        if len(prompt_obj.failing_info) > 0 and self.role != "developer" and (len(extra_msgs) == 0 or cal_token(extra_msgs, role_msgs, role_prompt, prompt_obj.failing_info) < token_limit[self.model_name]):
            role_msgs += [{"role": "user", "content": "Failed Cases:\n"+prompt_obj.failing_info}]
        
        role_msgs += [{"role": "user", "content": role_prompt}]
        role_msgs += extra_msgs

        retry_msgs = []
        while count_limit > 0:
            response = self.launch(self.sys_msg + role_msgs + retry_msgs, temperature=temperature)
            if response is None or len(response) == 0:
                logging.warning(f"** No response Error!")
                return None
            if self.role == "analyzer":
                return response
            try:
                if self.role in ["localizer", "fixer", "developer"]:
                    return parse_code(response, self.role, self.lang)
                if self.role == "inputter":
                    return parse_pair(response)
            
            except Exception as e:
                logging.warning(f"**Exception triggered: {e}\nNow try again ({count_limit} trails remains)")
                retry_msgs = [{"role": "assistant", "content": str(response)}, 
                              {"role": "user", "content": get_retry_prompt(self.role)}]
                count_limit -= 1

        return None


                
                



        
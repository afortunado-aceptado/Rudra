import logging
import numpy as np
from agent import Agent
from prompt import Prompt
from runtest import get_run_results
from post_analyze.evaluate import gauge_localizer
from formulate import get_changes_of_code
from consts import get_backup_prompt, token_limit
from utils import cal_token

temperatures = [1, 0.7, 0.2]

class MultiRound():
    def __init__(self, model_name, role="fixer", lang="C") -> None:
        self.role = role
        self.lang = lang
        self.model_name = model_name
        self.max_token = token_limit[model_name] - 200
    
    def run(self, prompt_obj, repeating_round=3, feedback_round=3):
        if self.role == "localizer":
            return self.localize(prompt_obj, repeating_round=repeating_round)
        if self.role == "fixer":
            self.looping_fail_num = [np.inf] * (feedback_round + 1)
            response, corr_flag, info = self.coding(prompt_obj, repeating_round=repeating_round)
            if feedback_round == 0 or corr_flag:
                return response, corr_flag
            
            return self.feedback(prompt_obj, 
                                 repair=response["code"], 
                                 run_results=info[0],
                                 compile_message=info[1],
                                 feedback_round=feedback_round
                                )
        if self.role == "developer":
            return self.coding(prompt_obj, repeating_round=repeating_round)
        else:
            NotImplementedError
    
    def localize(self, prompt_obj: Prompt, repeating_round=3):
        results, metrics = [], []
        for c in range(repeating_round):
            agent = Agent(model_name=self.model_name, role=self.role, lang=self.lang, temperature=temperatures[c])
            response = agent.run(prompt_obj, temperature=temperatures[c])
            if response is None: 
                results.append(None); metrics.append(False)
                continue
            gt_location = prompt_obj.get_gt_buggy_lines()
            tp, _, fn = gauge_localizer(gt_location, response["buggy_line"])  
            print(f"(tp:{tp}, fn:{fn})", response["buggy_line"], "<===>", gt_location)
            
            if tp/(tp+fn) > 0.5: 
                return response, True
            
            results.append(response)
            metrics.append(tp/(tp+fn) > 0.5)
        
        logging.warning("Cannot get satisfying localization!")
        return results[np.argmin(metrics)], False
    
    def coding(self, prompt_obj, repeating_round=3): #fixer and developer
        responses, looping_run_results, looping_compile_msgs = [], [], []
        for c in range(repeating_round):
            logging.info(f"Running at the round {c} ...")
            agent = Agent(model_name=self.model_name, role=self.role, lang=self.lang, temperature=temperatures[c])
            response = agent.run(prompt_obj, temperature=temperatures[c])
            if response is None: 
                responses.append(None); looping_compile_msgs.append(""); looping_run_results.append([None]*200)
                continue
            
            (run_results, compile_message) = get_run_results(response["code"], prompt_obj, early_stop=True)
            if len(run_results) == 0:
                logging.info(f"Correct code at the {c} repeating round -- {self.role}")
                return response, True, ([], "")
            
            responses.append(response)
            looping_run_results.append(run_results)
            looping_compile_msgs.append(compile_message)
        
        logging.warning(f"Cannot get the correct code -- {self.role}")
        best_idx = np.argmin([len(r) for r in looping_run_results])
        self.looping_fail_num[0] = len(looping_run_results[best_idx])
        return responses[best_idx], False, (looping_run_results[best_idx], looping_compile_msgs[best_idx])
    
    def feedback(self, prompt_obj: Prompt, repair: str, run_results: list[str], compile_message="", feedback_round=3):
        agent = Agent(model_name=self.model_name, role=self.role, lang=self.lang, temperature=1.0)
        
        for c in range(1, feedback_round + 1):
            logging.info(f"Feedback-supported looping at round {c}")
            sorted_run_results = [run_results[i] for i in np.argsort([len(res) for res in run_results])]
            changes = "\n".join(get_changes_of_code(prompt_obj.program, repair))
            if len(changes) == 0:
                assist_msgs = [{"role": "assistant", "content": "<actually repaired nothing>"}]
                user_msgs = [{"role": "user", "content": f"You didn't make any changes!"}]
            else:
                if cal_token(repair, prompt_obj.basic_token) > self.max_token and cal_token(changes, prompt_obj.basic_token) < self.max_token:
                    assist_msgs = [{"role": "assistant", "content": changes}]
                else:
                    assist_msgs = [{"role": "assistant", "content": repair}]

                if len(compile_message) > 0: #compile error
                    user_msgs = [{"role": "user", "content": f"Your repairing faces an compiling issue {compile_message}"}]
                else:
                    run_result_info = ''
                    for num, res in enumerate(sorted_run_results):
                        if cal_token(run_result_info, res, prompt_obj.basic_token, assist_msgs) < self.max_token - 1000:
                            run_result_info += f"#{num+1}\n{res}\n"
                        else:
                            logging.warning(f"Provide {num} failed cases out of {len(run_results)} due to token limitation.")
                            break
                    user_msgs = [{"role": "user", "content": f"Your repaired code fail on the following test cases:\n" + run_result_info}]
            
            response = agent.run(prompt_obj, 
                                extra_msgs=user_msgs+assist_msgs+[{"role":"user", "content":get_backup_prompt("feedback")}],
                                temperature=1
                                )
            if response is None:
                logging.warning(f"No response, stop at {c}")
                return {"code": repair, "explaination": ""}, False
            
            repair = response["code"]
            (run_results, compile_message) = get_run_results(repair, prompt_obj, early_stop=True)
            self.looping_fail_num[c]= len(run_results)
            if len(run_results) == 0:
                logging.info(f"It works at the {c} round!")
                return response, True
        
        logging.info(f"It doesn't work finally!")
        return response, False



            
            
            
            
            
        


    
    
            
            

            


    

import os
from utils import *
import logging
import sys
from prompt import Prompt
from multi_round import MultiRound
from agent import Agent

import time
from consts import lang2file, token_limit
import argparse
parser = argparse.ArgumentParser()

accessible_roles = ["inputter", "localizer", "fixer", "analyzer", "developer"]

parser.add_argument("--tracking", default=True, type=lambda x: x.lower() == "true")
parser.add_argument("--lang", default="Java", type=str)
parser.add_argument("--main_dir", default="../ConDefects", type=str)
parser.add_argument("--model_name", default="gpt-3.5-turbo-0125", choices=list(token_limit.keys()))
parser.add_argument("--program_type", default="raw", choices=["raw", "labeled", "agent-output", "empty"])
parser.add_argument("--roles", default=["fixer"], type=str, nargs='+')
parser.add_argument("--correct_reference", action="store_true")
parser.add_argument("--localization_exp", action="store_true")
parser.add_argument("--record_dir", default=None, type=str)
parser.add_argument("--resID", default=None, type=str)
parser.add_argument("--style", default="multi-round", choices=["agent", "synergy", "multi-round"], 
                            help='''
                                Agent: run a sequence of agents with a single round once called.
                                Synergy: run multiple interactive agents with a single round once called.
                                Multi-round: run a single agent for multiple rounds once called.
                                - NOTE: for one agent with one round, using agent and multi-round is both ok, but multi-round provides testing
                            ''')

parser.add_argument("--repeating_round", default=3, type=int)
parser.add_argument("--feedback_round", default=0, type=int)
#parser.add_argument("--note", default="", type=str)
parser.add_argument("--limit", default=1, type=int)
parser.add_argument("--case_limit", default=-1, type=int)


params = vars(parser.parse_args())

class Launch:
    def __init__(self, 
                 main_dir: str, 
                 model_name: str,
                 style: str,
                 roles: list[str] = ["fixer"], 
                 lang="Java",
                 program_type="raw",
                 correct_reference: bool = False, # Provide a correct code as reference?
                 localization_exp: bool = False, # Provide a previsouly obtained explaination of localization for repairing?
                 record_dir = None,
                 resID = None, # The hashid of the upstream agent's results
                 **kwargs
                 ):
        
        self.main_dir = main_dir
        self.model_name = model_name
        self.style = style
        self.roles = roles
        self.lang = lang
        self.program_type = program_type if "localizer" not in roles else "raw"
        self.correct_reference = correct_reference
        self.localization_exp = localization_exp
        self.resID = resID
        self.__assertion__()

        if record_dir is None:
            self.record_dir, self.hash_id = dump_exp(self.main_dir, params)
        else:
            #pre_exp_info = read_json(os.path.join(record_dir, "description.json"))
            #assert pre_exp_info == exp_info, "".join(Differ().compare(pre_exp_info, exp_info))
            self.record_dir, self.hash_id = record_dir, record_dir.split("/")[-1]
            logging_activate(record_dir)

        self.get_status_lst(correct_reference)

    def __assertion__(self):
        for role in self.roles:
            assert role in accessible_roles
        if self.style == "multi-round" and self.roles[-1] == "fixer": # QuixBugs only contain function-level code that cannot be directly executed, 
            assert not self.main_dir.lower().endswith("quixbugs")     # so we don't support on-line run information feedback currently
        if self.program_type == "empty": assert self.roles[0] == "developer"
        if self.program_type == "agent-output": assert self.resID is not None
        if self.localization_exp: assert self.program_type == "agent-output"
    
    def get_status_lst(self, correct_reference=False):
        self.sample_lst = return_lines(os.path.join(self.main_dir, f"Stat/{self.lang.lower()}_sample.txt"))
        self.existing_lst = return_lines(os.path.join(self.record_dir, "worked_lst.txt"))
        self.failed_lst = return_lines(os.path.join(self.record_dir, "failed_lst.txt")) #GPT cannot output results
        self.accept_lst = return_lines(os.path.join(self.record_dir, "accepted_lst.txt"))
        self.ignore_lst = return_lines(os.path.join(self.main_dir, "wrong_answer_cases.txt")) # No correct answers.        
        if correct_reference:
            self.ignore_lst += return_lines(os.path.join(self.main_dir, "no_reference_list.txt"))   
        
    def jumpover_condition(self, dir_info: str):
        os.sep='/'
        if ".DS_Store" in dir_info: return True
        # if len(self.sample_lst) > 0 and dir_info not in self.sample_lst:
        #     return True
        if "quixbugs" in self.main_dir.lower():
            return False
        [contest, _, _] = dir_info.split(os.sep)
        if not os.path.exists(os.path.join(self.main_dir, "Desc", contest+".txt")):
            logging.warning(f"Description {contest} doesn't exist!") 
            with open(os.path.join(self.main_dir, "no_desc.txt"), "a+") as wf:
                wf.write(contest+"\n")
            return True
        if not os.path.exists(os.path.join(self.main_dir, "Test", contest.split('_')[0], contest.split('_')[1].upper())):
            logging.warning(f"Test cases {contest} doesn't exist!") 
            return True
        if not os.path.exists(os.path.join(self.main_dir, "Code", dir_info)): 
            logging.warning(f"{dir_info} doesn't exist!")
            return True
        if not os.path.exists(os.path.join(self.main_dir, "Example", contest+".txt")):
            logging.warning(f"Example {contest} doesn't exist!") 
            return True
        if dir_info in self.ignore_lst + self.existing_lst + self.failed_lst:
            return True
        return False

    def save(self, response_dict: dict, dir_info: str):
        os.sep='/'
        if "quixbugs" in self.main_dir.lower():
            file_name = dir_info.split(os.sep)[0]
            dir_info = self.hash_id
        else:
            file_name = self.hash_id

        contest = dir_info.split(os.sep)[0]
        if "inputter" in self.roles:
            if response_dict["inputter"] is not None:
                os.makedirs(os.path.join(self.main_dir, "Gene-Test", contest), exist_ok=True)
                json_pretty_dump(response_dict["inputter"], 
                             os.path.join(self.main_dir, "Gene-Test", contest, f"{file_name}.json"))
                write_line(os.path.join(self.record_dir, "worked_lst.txt"), contest)
                return True
            else:
                write_line(os.path.join(self.record_dir, "failed_lst.txt"), contest)
                return False
        
        result_ok = sum([(v is not None) for v in response_dict.values()]) > 0
        aim_dir = os.path.join(self.main_dir, "Response", dir_info)
        os.makedirs(aim_dir, exist_ok=True)
        
        filename_dict = {"fixer": file_name, "developer": "code_"+file_name}
        for key in ["fixer", "developer"]:
            if response_dict[key] is None: continue
            with open(f"{aim_dir}/{filename_dict[key]}.{lang2file[self.lang]}", "w") as wf:
                try:
                    wf.write(response_dict[key]["code"])
                except Exception as e:
                    print(e)
                    print(key)
                    print(response_dict)
                    sys.exit()
                if self.lang in ["C", "Java"]:
                    wf.write("\n/* "+response_dict[key]["explaination"]+" */")
                elif self.lang == "Python":
                    wf.write("\n'''\n"+response_dict[key]["explaination"]+"\n'''")
        
        if response_dict["localizer"] is not None:
            json_pretty_dump(response_dict["localizer"], f"{aim_dir}/{file_name}.json")
        
        if response_dict["analyzer"] is not None:
            with open(f"{aim_dir}/{file_name}.txt", "w") as wf:
                wf.write(response_dict["analyzer"])
        
        if "quixbugs" in self.main_dir.lower(): dir_info = file_name
        if result_ok:
            write_line(os.path.join(self.record_dir, "worked_lst.txt"), dir_info)
        else:
            logging.warning(f"Cannot obtain response of {dir_info}!")
            write_line(os.path.join(self.record_dir, "failed_lst.txt"), dir_info)

        return result_ok
    #mimic multi_run.coding,get the code from agent.run and put it into test,the tempatature is solid,maybe it could be improved
    def agent_coding(self, prompt_obj): #fixer,除了使用parse_code得到正确代码，还要进行测试
        role="fixer"
        agent = Agent(model_name=self.model_name, role=role, lang=self.lang, temperature=0.7)
        response = agent.run(prompt_obj, temperature=0.7)
        if response is None: 
            response=None;compile_msgs=""; run_results=[None]*200
        (run_results, compile_msgs) = get_run_results(response["code"], prompt_obj, early_stop=True)
        if len(run_results) == 0:
            logging.info(f"Correct code at agent round -- {role}")
            return response, True, ([], "")
        logging.warning(f"Cannot get the correct code -- {role}")
        #因为agent不需要轮询并且调整，所以直接返回一个好嘞
        return response, False, (run_results,compile_msgs)
       
    def run_agent(self, prompt_obj: Prompt):
        response_dict = {k: None for k in accessible_roles}
        for rid, role in enumerate(self.roles):
             #when role==fixer,add runtest and return corr_flag
            if role == "fixer":
                response, corr_flag, info =self.agent_coding(prompt_obj)
                response_dict[role] = response
                if corr_flag:
                    return response_dict, corr_flag
            response = Agent(role=role, model_name=self.model_name).run(prompt_obj)
            response_dict[role] = response
            if rid != len(self.roles) -1:
                prompt_obj.update_prompt(updated_info=response)
            time.sleep(5)
        return response_dict, False

    def run_multiround(self, prompt_obj: Prompt, dir_info: str, repeating_round=3, feedback_round=3): 
        response_dict = {k: None for k in accessible_roles}
        multiround = MultiRound(role=self.roles[0], lang=self.lang, model_name=self.model_name)
        response_dict[self.roles[0]], accept_flag = multiround.run(prompt_obj, 
                                                                repeating_round=repeating_round, 
                                                                feedback_round=feedback_round)

        if feedback_round > 0 and self.roles[0] == "fixer":
            with open(os.path.join(self.record_dir, 'looping_info.tsv'), 'a+') as tsvfile:
                tsvfile.write(f"{dir_info}\t{len(prompt_obj.failed_cases)}\t")
                tsvfile.write("\t".join([str(multiround.looping_fail_num[k]) for k in range(feedback_round+1)]))
                tsvfile.write("\n")

        return response_dict, accept_flag
    
    def run(self, repeating_round=3, feedback_round=0, limit=-1, case_limit=-1, **kwargs):
        worked_num = len(self.existing_lst)
        
        if feedback_round > 0: 
            assert self.style == "multi-round" and self.roles[0] == "fixer"
            with open(os.path.join(self.record_dir, 'looping_info.tsv'), 'w+') as tsvfile:
                tsvfile.write("Directory\tSubmissionFailedNum\t")
                tsvfile.write("\t".join([f"NewFailedNum_{k}" for k in range(feedback_round+1)]))
        
        for contest in sorted(os.listdir(os.path.join(self.main_dir, "Code"))):
            if contest in (self.existing_lst + self.failed_lst + [".DS_Store"]): continue
            if not os.path.exists(os.path.join(self.main_dir, "Code", contest, self.lang)): 
                continue
            #inputter works on a problem level
            
            for sub_id in os.listdir(os.path.join(self.main_dir, "Code", contest, self.lang)):
                if limit > 0 and worked_num >= limit: return
                dir_info = f"{contest}/{self.lang}/{sub_id}"
                if self.jumpover_condition(dir_info): continue
                
                logging.info(f"{'^'*5} {dir_info} @{self.hash_id} {'^'*5} {worked_num}")

                try:
                    prompt_obj = Prompt(self.main_dir, 
                                    dir_info,
                                    program_type=self.program_type, 
                                    correct_reference=self.correct_reference,
                                    localization_exp=self.localization_exp,
                                    resID=self.resID,
                                    max_token=int(token_limit[self.model_name] * 0.7),
                                    case_limit=case_limit,
                                )
                except UserWarning as e:
                    print(">>>>", e)
                    logging.warning(f"Cannot directly handle {dir_info}, waiting for special processing")
                    write_line(os.path.join(self.record_dir, "failed_lst.txt"), dir_info)
                    continue
                
                if self.style == "agent":
                    response_dict, pass_cases_flag = self.run_agent(prompt_obj)
                elif self.style == "multi-round":
                    response_dict, pass_cases_flag = self.run_multiround(prompt_obj, 
                                                                dir_info, 
                                                                repeating_round=repeating_round, 
                                                                feedback_round=feedback_round)
                elif self.style == "synergy":
                    NotImplementedError
                
                if pass_cases_flag and (dir_info not in self.accept_lst):
                    self.accept_lst.append(dir_info)
                    write_line(os.path.join(self.record_dir, "accepted_lst.txt"), dir_info)

                worked_num += self.save(response_dict, dir_info)

                if self.roles[-1] == "inputter": break

if __name__ == "__main__":
    launch = Launch(**params)
    launch.run(**params)
    
    wk_num = len(return_lines(os.path.join(launch.record_dir, 'worked_lst.txt')))
    acc_num = len(return_lines(os.path.join(launch.record_dir, 'accepted_lst.txt')))
    print(f"{acc_num}/{wk_num} submisstions are correct in {launch.record_dir}")

    if os.path.exists("exp_records.json"):
        record_dict = read_json("exp_records.json")
    else: record_dict = {}
    record_dict.update({launch.record_dir: f"{acc_num}/{wk_num}"})
    json_pretty_dump(record_dict, "exp_records.json")

    for file in os.listdir("./"):
        if file.endswith(".class") or file == "tmp.py" or file.endswith(".java") or file.endswith(".exec") or file.endswith(".c") or file.endswith(".out"):
            os.remove(file)
    
   
    

    

        



    

        
        

import os
import logging
from formulate import formulate_code
from utils import read_json
from consts import lang2file, lang2comm
import numpy as np


class Prompt:
    def __init__(self, main_dir, 
                 dir_info,
                 program_type="raw", 
                 correct_reference=False,
                 localization_exp=False,
                 resID=None,
                 max_token=4000,
                 case_limit=-1,
                 ) -> None:
        os.sep='/'
        [contest, lang, sub_id] = dir_info.split(os.sep)
        self.main_dir = main_dir
        self.contest = contest
        self.lang=lang
        self.sub_id = sub_id
        self.dir_info = dir_info
        self.failed_cases = []
    
        with open(os.path.join(main_dir, f"Desc/{contest}.txt")) as rf:
            self.description = rf.read().strip()
        with open(os.path.join(main_dir, f"Example/{contest}.txt")) as rf:
            self.example = rf.read().strip()

        self.get_program(program_type, resID=resID)

        self.basic_token = (len(self.description)+len(self.example)+len(self.program)) // 2
        if self.basic_token > max_token:
            raise UserWarning(f"Too long prompt! Description {len(self.description)//2}, Program {len(self.program) // 2}, Example {len(self.example) // 2}, Desc+Pro = {len(self.description)//2 + len(self.program) // 2}\n")
        
        self.failing_info = self.get_failing_info(limit_token=max_token-self.basic_token, case_limit=case_limit)
        if correct_reference:
            self.reference = self.get_reference()
        if localization_exp:
            assert resID is not None
            self.location_exp =  read_json(os.path.join(main_dir, "Response", dir_info, resID+".json"))["explaination"]

          
    def __get_all_failed_cases(self):
        cases = []
        if "quixbugs" in self.main_dir.lower():
            test_dir = f"Test/{self.contest}"
        else:
            test_dir = os.path.join(self.main_dir, f"Test/{self.contest.split('_')[0]}/{self.contest.split('_')[1].upper()}")
        
        if not os.path.exists(os.path.join(self.main_dir, test_dir, "in")): return []
        for f in os.listdir(os.path.join(self.main_dir, test_dir, "in")):
            if not f.endswith(".txt"): continue  
            with open(os.path.join(self.main_dir, f"RealOut/{self.dir_info}/{f}")) as rf,\
                open(os.path.join(self.main_dir, test_dir, "out", f)) as ef:
                program_output = rf.read().strip()
                expected_output = ef.read().strip()
            
            if program_output != expected_output:
                with open(os.path.join(self.main_dir, test_dir, "in", f)) as inpf:
                    program_input = inpf.read().strip()
                cases.append("Input:\n"+program_input+"\nProgram Output:\n"+program_input+"\nExpected Output:\n"+expected_output)
        
        self.failed_cases = [cases[i] for i in np.argsort([len(c) for c in cases])]

    def get_failing_info(self, limit_token=3000, case_limit=-1):
        if len(self.failed_cases) == 0:
            self.__get_all_failed_cases()
        
        failed_case_str = ''
        for num, case_str in enumerate(self.failed_cases):
            if case_limit > 0 and num >= case_limit: break
            if len(failed_case_str) + len(case_str) < limit_token * 2:
                failed_case_str += f"#{num+1}\n{case_str}\n"
            else:
                logging.warning(f"Provide {num} failed cases out of {len(self.failed_cases)} due to token limitation ({limit_token}).")
                break
        
        return failed_case_str
    
    def get_program(self, _type="raw", resID=None):
        self.program = f"```{self.lang}\n"
        os.sep='/'
        if _type == "raw":
            self.program += formulate_code(self.lang, remove_comment=True, input_is_file=True,
                                           _input=os.path.join(self.main_dir, "Code", self.dir_info, "faultyVersion."+lang2file[self.lang])
                                        )+"\n```"
        elif _type == "labeled": # has been formulated
            with open(os.path.join(self.main_dir, "Code", self.dir_info, "faultyLabeled."+lang2file[self.lang])) as f:
                self.program += f.read().strip()+"\n```"
        
        elif _type == "agent-output":
            if "quixbugs" in self.main_dir.lower():
                json_path = os.path.join(self.main_dir, "Response", resID, self.dir_info.split(os.sep)[0]+".json")
            else:
                json_path = os.path.join(self.main_dir, "Response", self.dir_info, resID+".json")
            if not os.path.exists(json_path):
                raise UserWarning(f"{json_path} does not exist!\n")
            self.program += read_json(json_path)["refined_labeled_code"]+"\n```"
       
        elif _type == "empty":
            self.program = ""
    
    def get_gt_buggy_lines(self):
        buggy_lines = []
        with open(os.path.join(self.main_dir, "Code", self.dir_info, "faultyLabeled."+lang2file[self.lang])) as f:
            for c in f.read().strip().splitlines():
                if lang2comm[self.lang] in c and ("Buggy" in c or "buggy" in c):
                    buggy_lines.append(c.split(lang2comm[self.lang])[0].strip())
        return buggy_lines
    
    def get_reference(self):
        NotImplementedError

    def update_prompt(self):
        NotImplementedError
    

        

        
            
                



from pathlib import Path
import os
import logging
import sys
import time
sys.path.append("..")
import runtime

def get_run_results(code, prompt_obj, early_stop=False):
    compile_message = runtime.compile_from_code(code, prompt_obj.lang)
    abs_path = str(Path().absolute())
    if prompt_obj.lang == "Python":
        run_command = compile_message
    else:
        run_command = runtime.get_run_command(abs_path, prompt_obj.lang)
    
    test_dir = f"{prompt_obj.main_dir}/Test/{prompt_obj.contest.split('_')[0]}/{prompt_obj.contest.split('_')[1].upper()}"
    i = 0
    wrong_results, empty_output = [], []
    t0 = time.time()
    for testcase in sorted(os.listdir(os.path.join(test_dir, "in"))):
        if not testcase.endswith("txt"): continue
        output_file = os.path.join(abs_path, test_dir, "out", testcase)
        if not os.path.exists(output_file): continue
        input_file = os.path.join(abs_path, test_dir, "in", testcase)
        i += 1
        try:
            program_output = runtime.run_a_case(input_file, run_command, prompt_obj.lang)
        except Exception as e:
            print("Error during testing -> ", str(e))
        
        result = runtime.validate_output(program_output, output_file)
        
        if len(program_output.strip()) == 0:
            empty_output.append(testcase)
            program_output = "<Error: Empty output>"
            add_print = "Empty"
        else: add_print = ""
        print("Running", testcase, (result == "Accepted"), add_print)
        t = time.time()-t0

        if result != "Accepted":
            with open(input_file, "r") as in_f, open(output_file, 'r') as out_f:
                wrong_results.append("\n".join([
                    "Input: " + in_f.read().strip(), 
                    "Program Output: " + program_output.rstrip('\n'),
                    "Expected Output: " + out_f.read().rstrip('\n')
                ]))
            if early_stop and i >= 5 and t >= 300:
                return (wrong_results, compile_message)
    
    if len(empty_output) == i:
        logging.warning("Empty output")
    
    return (wrong_results, compile_message)

if __name__ == "__main__": # unit testing
    response_code_path = sys.argv[1]

    class temp_obj:
        def __init__(self, lang, main_dir, contest):
            self.lang = lang
            self.main_dir = main_dir
            self.contest = contest

    with open(response_code_path) as rf:
        code = rf.read()
    os.sep='/'
    idx = response_code_path.find("Response")
    if idx == -1: idx = response_code_path.find("Code")
    main_dir = response_code_path[:idx]
    contest = response_code_path[idx:].split(os.sep)[1]
    lang = response_code_path[idx:].split(os.sep)[2]

    obj = temp_obj(lang, main_dir, contest)
    get_run_results(code, obj)

    




    

    
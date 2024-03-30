import os
import subprocess
from pathlib import Path
import shutil
import sys

def run_compile(compile_command):
    try:
        return subprocess.run(compile_command, 
                                        shell=True, 
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        timeout=10).stdout.decode("utf-8")

    except subprocess.TimeoutExpired:
        return "Compile Timeout"

def compile_from_path(code_path):
    if code_path.endswith(".java"):
        compile_command = "javac Main.java"
        shutil.copy(code_path, "Main.java")
    elif code_path.endswith(".c"):
        compile_command = "clang "+ code_path 
    elif code_path.endswith(".py"):
        with open(code_path, 'r', encoding='utf-8',errors='ignore') as f:
            code = f.read()
        with open("tmp.py", "w") as wf:
            wf.write(code)
        if "print " in code:
            return "/Users/libaitong/opt/anaconda3/condabin/conda run -n py27 python tmp.py" 
        else: return "python3 tmp.py"
    else:
        raise NotImplementedError("Not implemented", code_path)
    return run_compile(compile_command)
   
def compile_from_code(code, lang):
    if lang == "Python": 
        with open("tmp.py", "w") as wf:
            wf.write(code)
        if "print " in code:
            return "/Users/libaitong/opt/anaconda3/condabin/conda run -n py27 python tmp.py" 
        else: return "python3 tmp.py"
    if lang == "Java":
        with open("Main.java", "w") as wf:
            wf.write(code.strip())
        compile_command = "javac Main.java"
    elif lang == "C":
        with open("main.c", "w") as wf:
            wf.write(code.strip())
        compile_command = "clang main.c"
    else:
        NotImplementedError
        sys.exit()
    return run_compile(compile_command)

def run_a_case(test_case_input_path, run_command, lang="Python"):# after compiling
    with open(test_case_input_path, 'r') as input_handle:
        try:
            run_process = subprocess.run(run_command,
                                        stdin=input_handle,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        timeout=120 if lang=="Python" else 60,
                                        shell=True)
            return run_process.stdout.decode("utf-8", "ignore")
        except subprocess.TimeoutExpired:
            return "Run Timeout"
        except Exception as e:
            print(e)
            return "Runtime Error " +  e

def validate_output(program_output: str, output_file, show=False):
    with open(output_file, 'r', encoding='utf-8',errors='ignore') as f:
        expected_output = f.read().rstrip("\n").splitlines()
    
    if program_output.startswith("Runtime Error"):
        return program_output
    elif program_output.startswith("./"):
        return "Execution Error"
    else:
        program_output = program_output.rstrip("\n").splitlines()
        if len(program_output) != len(expected_output):
            return "Wrong Answer"
        for (a, b) in zip(program_output, expected_output):
            if a.strip() != b.strip():
                if show:
                    print(program_output, "|", expected_output)
                return "Wrong Answer"
    return "Accepted"

def get_run_command(abs_path, lang):
    if lang == "Java":
        return f"java -javaagent:{abs_path}/lib/jacocoagent.jar=destfile=jacoco.exec -cp {abs_path} Main"
    elif lang == "C":
        return "./a.out"
    elif lang == "Python":
        return

def get_lack_gt_repair(code_dir, test_case_dir):
    lang2file = {"C": "c", "Java":"java", "Python": "py"}
    [main_dir, _, codeID, lang, sub_dir] = code_dir.split(os.sep)
    code_file = "correctVersion."+lang2file[lang]
   
    ### 检查description: 是否存在，是否允许多重输出
    if not os.path.exists(os.path.join(main_dir, "Desc", codeID+".txt")):
        with open(os.path.join(main_dir, "Stat", "lack_desc.txt"), "a+") as wf:
            wf.write(f"{codeID}/{lang}/{sub_dir}\n")
        return
    with open(os.path.join(main_dir, "Desc", codeID+".txt")) as rf:
        desc = rf.read()
    for symbol in ["find any", "print any", "output any"]:
        if symbol in desc:
            with open(os.path.join(main_dir, "Stat", "multi_ans_desc.txt"), "a+") as wf:
                wf.write(f"{codeID}/{lang}/{sub_dir}\n")
            return
    
    abs_path = str(Path().absolute())
    try:
        compile_message = compile_from_path(os.path.join(str(Path().absolute()), code_dir, code_file))
    except Exception as e:
        print("Compiling error during testing -> ", str(e))
        return False
    
    if lang == "Python":
        run_command = compile_message
    else:
        run_command = get_run_command(abs_path, lang)

    empty_num = 0
    results, omit_case = [], []
    for testcase in sorted(os.listdir(os.path.join(test_case_dir, "in"))):
        if not testcase.endswith("txt"): continue
        output_file = os.path.join(abs_path, test_case_dir, "out", testcase)
        if not os.path.exists(output_file): continue
        input_file = os.path.join(abs_path, test_case_dir, "in", testcase)

        program_output = run_a_case(input_file, run_command)
        if len(program_output.strip()) == 0:
            empty_num += 1
            result = "Wrong Answer"
        else:
            result = validate_output(program_output, output_file)
        
        correct_flag = (result == "Accepted")
        results.append(correct_flag)
        #print("checking", testcase, correct_flag)

        if not correct_flag:
            with open(input_file) as rf:
                desc = rf.read().strip()
                if desc.endswith("...") and len(desc) > 50:
                    omit_case.append(testcase)
                else: 
                    with open(os.path.join(main_dir, "Ignore", "no_gt_repair.txt"), "a+") as wf:
                        wf.write(f"{codeID}/{lang}/{sub_dir}\n")
                    return False #的确出错了
    
    # 无testcase
    if len(results) == 0:
        with open(os.path.join(main_dir, "Stat", "no_test_case.txt"), "a+") as wf:
            wf.write(f"{codeID}/{lang}/{sub_dir}\n")
        return True
    #全部都是empty，可能是编译/环境问题
    if empty_num == len(results) and empty_num > 0:
        with open(os.path.join(main_dir, "Stat", "empty_gt.txt"), "a+") as wf:
            wf.write(f"{codeID}/{lang}/{sub_dir}\n")
        return True
    #ground truth repair 是正确的
    if len(results) - sum(results) == 0: 
        with open(os.path.join(main_dir, "Stat", "correct_gt.txt"), "a+") as wf:
            wf.write(f"{codeID}/{lang}/{sub_dir}\n")
        return True 
    
    #出错完全是因为test case 中含有省略号
    if len(omit_case) == (len(results) - sum(results)) and len(omit_case) < len(results):
        for testcase in omit_case:
            os.remove(os.path.join(abs_path, test_case_dir, "in", testcase))
            os.remove(os.path.join(abs_path, test_case_dir, "out", testcase))
        with open(os.path.join(main_dir, "Stat", "omit_cases.txt"), "a+") as wf:
            wf.write(f"{codeID}/{lang}/{sub_dir}\t"+','.join(omit_case)+"\n")
    return True

def run_results_from_path(code_dir,
                        test_case_dir, 
                        lang,
                        code_file="correctVersion.py",
                        style="check_gt",
                        record_dir=None):
    
    if not os.path.exists(code_dir):
        raise ValueError(f"{code_dir} doesn't exist")

    if style == "get_gt": #数据集中有一些input file缺少对应的output file
        assert code_file.startswith("correct")
        lack_gt_res = []
        for testcase in sorted(os.listdir(os.path.join(test_case_dir, "in"))):
            if testcase.endswith("txt") and (not os.path.exists(os.path.join(test_case_dir, "out", testcase))):
                lack_gt_res.append(testcase)
        if len(lack_gt_res) == 0: return 
    
    abs_path = str(Path().absolute())
    try:
        compile_message = compile_from_path(os.path.join(str(Path().absolute()), code_dir, code_file))
    except Exception as e:
        print("Compiling error during testing -> ", str(e))
        return False
    
    if lang == "Python":
        run_command = compile_message
    else:
        run_command = get_run_command(abs_path, lang)

    if style == "check_gt": #检查数据集给定的ground-truth是否能pass所有已知的test case
        assert code_file.startswith("correct")
        
        for testcase in sorted(os.listdir(os.path.join(test_case_dir, "in"))):
            if not testcase.endswith("txt"): continue
            output_file = os.path.join(abs_path, test_case_dir, "out", testcase)
            if not os.path.exists(output_file): continue
            print("checking", testcase)
            program_output = run_a_case(os.path.join(abs_path, test_case_dir, "in", testcase), run_command)
            if len(program_output) == 0 or not (validate_output(program_output, output_file) == "Accepted"):
                return 0     
        return 1
    
    if style == "get_gt": #数据集中有一些input file缺少对应的output file                
        for testcase in lack_gt_res:
            input_file = os.path.join(abs_path, test_case_dir, "in", testcase)
            output_file = os.path.join(abs_path, test_case_dir, "out", testcase)
            print("Getting", testcase)
            try:
                program_output = run_a_case(input_file, run_command)
            except Exception as e:
                print("Error during testing -> ", str(e))
                return -1
            if len(program_output) == 0: return -1       
            with open(os.path.join(abs_path, test_case_dir, "out", testcase), "w") as wf:
                wf.write(program_output)
        return 1
    
    if style == "simple": #单纯想跑结果
        if record_dir is not None:
            os.makedirs(record_dir, exist_ok=True)
        
        zero_output, count = 0, 0
        wrong_testcase = []
        for testcase in sorted(os.listdir(os.path.join(test_case_dir, "in"))):
            if not testcase.endswith("txt"): continue
            input_file = os.path.join(abs_path, test_case_dir, "in", testcase)
            output_file = os.path.join(abs_path, test_case_dir, "out", testcase)
            if not os.path.exists(output_file): continue
            
            count += 1
            try:
                program_output = run_a_case(input_file, run_command)
            except Exception as e:
                print("Error during testing -> ", str(e))
                return False
            
            if record_dir is not None:
                with open(os.path.join(record_dir, testcase), "w") as wf:
                    wf.write(program_output)
            
            if len(program_output.strip()) == 0:
                print("Running", testcase, "Empty output")
                return False
            elif validate_output(program_output, output_file) != "Accepted":
                print("Running", testcase, "False")
                return False
            print("Running", testcase, "True")
        
        return True

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--main_dir", default="ConDefects", type=str)
    parser.add_argument("--lang", default="C", type=str)
    params = vars(parser.parse_args())

    main_dir, lang = params["main_dir"], params["lang"]
    done = []
    if os.path.exists("done"):
        with open("done") as rf:
            done = rf.read().splitlines()
    
    c = len(done)
    for codeID in os.listdir("aaa"):
        if os.path.exists("aaa/"+codeID+"/C"):
            for subID in os.listdir("aaa/"+codeID+"/C"):
                dir_info = f"{codeID}/C/{subID}"
                if dir_info in done: continue
                print("#####", dir_info, c)
                c += 1
                [contestName, contestID] = codeID.split('_')
                flag = run_results_from_path(
                    code_dir="aaa/"+dir_info,
                    test_case_dir=f"CodeFlaws/Test/{contestName}/{contestID.upper()}",
                    code_file="c36762f9.c",
                    lang="C",
                    style="simple"
                )
                if flag:
                    with open("accepted_lst.txt", "a+") as wf:
                        wf.write(dir_info+"\n")
                    with open("done", "a+") as wf:
                        wf.write(dir_info+"\n")

    # correct = []
    # if os.path.exists(os.path.join(main_dir, f"Stat/{lang}_correct_gt.txt")):
    #     with open(os.path.join(main_dir, f"Stat/{lang}_correct_gt.txt")) as rf:
    #         correct = rf.read().splitlines()
    # done = set(done) | set(correct)
    
    # print(len(done))
    # for i, codeID in enumerate(sorted(os.listdir(os.path.join(main_dir, "Code")))):
    #     if "Store" in codeID: continue
    #     if not os.path.exists(os.path.join(main_dir, "Code", codeID, lang)): continue
    #     print(f"^^^^^ {i+1}/{len(os.listdir(os.path.join(main_dir, 'Code')))}",  codeID)
    #     for sub_dir in os.listdir(os.path.join(main_dir, "Code", codeID, lang)):
    #         if "Store" in sub_dir: continue
    #         if f"{codeID}/{lang}/{sub_dir}" in done: continue
    #         [contestName, contestID] = codeID.split('_')
            
    #         gt_exist = get_lack_gt_repair(f"{main_dir}/Code/{codeID}/{lang}/{sub_dir}", 
    #                                       f"{main_dir}/Test/{contestName}/{contestID.upper()}")
            
    #         if gt_exist is None: gt_exist = "None"
    #         print("#####", sub_dir, gt_exist)
    #         with open("done", "a+") as wf:
    #             wf.write(f"{codeID}/{lang}/{sub_dir}\n")
    
    



            
            
            
        
            


            






            
            

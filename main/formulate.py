import subprocess
import os
import re
from consts import lang2file
from difflib import ndiff

def formulate_code(lang, _input, remove_comment=False, input_is_file=True):
    if input_is_file:
        with open(_input) as rf:
            code = rf.read()
    else: code = _input
    with open("tmp."+lang2file[lang], "w") as wf:
        if remove_comment:
            wf.write(comment_remover(code, lang))
        else:
            wf.write(code)
    
    if lang in ["C", "Java"]:
        with open("tmp."+lang2file[lang]) as f:
            out = subprocess.run("clang-format -style=file", 
                        stdin=f, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        timeout=10,
                        shell=True).stdout.decode("utf-8")
    elif lang == "Python":
        subprocess.run(f"python -m black -S tmp.py",
                        stderr=subprocess.PIPE,
                        timeout=10,
                        shell=True)
        with open("tmp.py") as rf:
            out = rf.read()
    os.remove("tmp."+lang2file[lang])
    return "\n".join([o.rstrip() for o in out.splitlines() if len(o.rstrip()) > 0])

def comment_remover(code, lang):
    if lang in ["C", "Java"]:
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'^\s*$', '', code, flags=re.MULTILINE) #Remove empty lines
        return code 
    if lang == "Python":
        code = re.sub(r'\'\'\'.*?\'\'\'', '', code, flags=re.DOTALL)
        code = re.sub(r'#.*', '', code)
        code = re.sub(r'^\s*$', '', code, flags=re.MULTILINE) #Remove empty lines
        return code 

    
def get_changes_of_code(original, current, lang="C"):
    with open("original."+lang2file[lang], "w") as wf:
        wf.write(comment_remover(original, lang))
    original_format = formulate_code(lang, "original."+lang2file[lang])
    os.remove("original."+lang2file[lang])

    with open("current."+lang2file[lang], "w") as wf:
        wf.write(comment_remover(current, lang))
    current_format = formulate_code(lang, "current."+lang2file[lang])
    os.remove("current."+lang2file[lang])

    o = [s.rstrip() for s in original_format.splitlines() if len(s.strip()) > 0]
    c = [s.rstrip() for s in current_format.splitlines() if len(s.strip()) > 0]
    return [line for line in list(ndiff(o, c)) if line[0] in ["+", "-"]]

    

    



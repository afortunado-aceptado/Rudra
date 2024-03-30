from consts import lang2comm
import logging
def extract_buggy_lines(code: str, lang="C") -> list[str]:
    res = []
    code_lines = code.splitlines()
    for i, l in enumerate(code_lines):
        if lang2comm[lang] in l and "buggy" in l.lower():
            if len(l.split(lang2comm[lang])[0].strip()) > 0:
                res.append(l.split(lang2comm[lang])[0].strip())
            elif i+1 < len(code_lines):
                res.append(code_lines[i+1].strip())
    return res

class ParseError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status

def parse_code(response, role, lang="C"):   
    import re
    code_lst = []
    for i, pattern in enumerate([r'```(?:[^\n]*\n)?(.*?)```', r'```(?:[^\n]*\n)?(.*?)\$\$', r'`(?:[^\n]*\n)?(.*?)`', r'```(?:[^\n]*\n)?(.*?)$']):
        code_lst = re.findall(pattern, response, re.DOTALL)
        if len(code_lst) > 0 and len(code_lst[0]) > 0:
            break
    if len(code_lst) == 0: #Cannot find valid code
        logging.error("Cannot extract any code")
        raise ValueError("Cannot extract any code")
    
    if role in ["fixer", "developer"]:
        code = code_lst[-1].strip()
    else:
        code = "\n".join([c.strip() for c in code_lst])
    if "$" in code:
        code = code[:code.find("$")].strip()
    
    exp_lst = []
    for pattern in [r'\$\$(?:[^\n]*\n)?(.*?)\$\$', r'\$\$(?:[^\n]*\n)?(.*?)$', r'^(?:[^\n]*\n)?(.*?)```']:
        exp_lst = re.findall(pattern, response, re.DOTALL)
        if len(exp_lst) > 0: break

    if len(exp_lst) == 0:
        logging.warning("This response doesn't explain the repairing")
        explaination = ""
    else:
        explaination = "\n".join(exp_lst)
    
    if role in ["fixer", "developer"]:
        return {"code": code, "explaination": explaination}
    if role == "localizer":
        return {"labeled_code": code, "explaination": explaination, "buggy_line": extract_buggy_lines(code, lang)}
    raise ValueError(f"Not identified role {role} during parsing code!")

def parse_pair(response):
    NotImplementedError
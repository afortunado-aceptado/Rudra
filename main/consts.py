token_limit = {"gpt-3.5-turbo-0125": 4000, 
               "gpt-4-0125-preview": 6000, 
               "gemini-pro": 6000, 
               "deepseek-coder": 6000,
               "Phind/Phind-CodeLlama-34B-v2": 6000,
               "google/gemma-7b-it": 5000,
               }

lang2file = {"C": "c", "Java":"java", "Python": "py"}
lang2comm = {"Java": "//", "C": "//", "Python": "#"}

def get_sys_prompt(role, lang, test_case_num=10):
    if role == "localizer":
        return "".join(["You are an assistant skilled in identifying functional bugs. ",
                        "Your goal is to label buggy code statements so that the code can be corrected by MERELY revising your identified code lines. ",
                        "Focus on the functionality and the input/output format (adhereing to the example format)"])
    
    if role == "fixer":
        return "".join(["You are a skilled assistant with expertise in program repair. Your task is to repair code snippets, ",
                        "ensuring they function correctly according to the given specifications and pass given test cases."])
    #Your repairing should ONLY make changes on the labeled buggy lines. \
    
    if role == "analyzer":
        return "".join(["You are a proficient assistant with expertise in code review. Your task is to analyze the provided code snippet and ",
                        "check its correctness of the functionality and the input/output format, based on the corresponding problem description."])
    
    if role == "inputter":
        return "".join(["Your role is to design and construct a detailed suite of test case inputs for specific programming problem. ",
                        "You must ensure that each test case input aligns with the input specifications and limitations. ",
                        "Your test cases should be diverse and thorough, aiming to reveal various semantic flaws and boundary condition issues. ",
                        "Besides typical inputs, please prioritize creating tests for: Boundary values (maximum/minimum); Unusually long inputs; Repetitive/identical inputs; Edge cases. ",
                        f"Based on the program description and input constraints, please generate more than {test_case_num} testing inputs (no outputs)"])

    if role == "developer":
        if lang == "Python": lang = "Python 3.7"
        return "".join(["You are an experienced developer tasked with programming for coding interview problems. Your task is to write correct, ", 
                        f"well-functioned {lang} code based on given specifications, also adhering to the required input/output format"])

    raise NotImplementedError

def get_role_prompt(role, lang="C", buggy_line_num=5, tracking=True):
    if role == "localizer":
        examples = {"C": '''For example, given
                                ```
                                #include <stdio.h>
                                int main(){cod
                                int c = 0;
                                printf("%d", a);
                                }
                                ```
                                You should return:
                                ```
                                #include <stdio.h>
                                int main(){
                                int c = 0;
                                printf("%d", a); // buggy line
                                }
                                ```
                                $$
                                The code defines an interger c but prints an undefined a, causing an error.
                                $$''',
                    "Java": '''For example, given
                                ```
                                public class Main {
                                public static void main(String[] args) {
                                int c = 0;
                                System.out.println(a);
                                }
                                }
                                ```
                                You should return:
                                ```
                                public class Main {
                                public static void main(String[] args) {
                                int c = 0;
                                System.out.println(a); // buggy line
                                }
                                }
                                ```
                                $$
                                The code defines an interger c but prints an undefined a, causing an error.
                                $$''',
                    "Python": '''For example, given
                                ```
                                c = 0
                                print(a)
                                ```
                                You should return:
                                ```
                                c = 0
                                print(a) # buggy line
                                }
                                }
                                ```
                                $$
                                The code defines an interger c but prints an undefined a, causing an error.
                                $$'''
        }
        comments = {"C": "// buggy line", "Java": "// buggy line", "Python": "# buggy line"}

        if tracking:
            return "".join(["Analyze the provided code against the failed test cases step by step; Pay attention to the input/output format; Explicitly track the values of key variables at critical points.  ",
                        f"Compare these values against the expected outcomes. Directly within the provided code, label NO MORE THAN {buggy_line_num} line(s) that you identify as the root cause of the bug(s) with a code comment. ",
                        f"Do this by adding the comment {comments[lang]} on the same line. Ensure the original code, with your annotations, is enclosed within three backticks (```) to maintain formatting. Do not return separate buggy lines. "
                        "After labeling, provide a brief explanation on how tracking key variable values at critical points helps in identifying bugs. Enclose this explanation within two dollar signs ($$) to differentiate it from the code. ",
                        examples[lang]])
        else:
            return "".join([f"Analyze the provided code against the failed test cases step by step; Directly within the provided code, label NO MORE THAN {buggy_line_num} line(s) that you identify as the root cause of the bug(s) with a code comment. ",
                        f"Do this by adding the comment {comments[lang]} on the same line. Ensure the original code, with your annotations, is enclosed within three backticks (```) to maintain formatting. Do not return separate buggy lines.",
                        examples[lang]])
    
    if role == "fixer":
        if tracking:
            return "".join(["Please repair the code to make it function well (solving the described problem), pass all test cases, and satisfy requirements (including input/output format, referring to the examples). ",
                        "Steps: Analyze the code against failed test cases step by step, particularly focusing on the labeled potential buggy line(s); Track critical parameter values and compare them to expected outcomes; ",
                        "Double-check the labeled buggy lines. Make minimal but essential changes on really faulty line(s). Objective: return the **COMPLETE** modified code, enclosed within three backticks (```), ",
                        "followed by a brief explaination on how tracking key parameter values guide your revisions. The explaination must be enclosed within two dollar signs ($$). No more any additional text!"])
        else:
            return "".join(["Please repair the code to make it function well (solving the described problem), pass all test cases, and satisfy requirements (including input/output format, referring to the examples). ",
                        "You should analyze the code against failed test cases step by step, particularly focusing on labeled potential buggy line(s), and then make minimal but essential changes on really faulty line(s). ",
                        "Objective: return the **COMPLETE** modified code, enclosed within three backticks (```). Then provide a brief explaination enclosed within two dollar signs ($$). No more any additional text!"])
    if role == "analyzer":
        return "Given the buggy code and its repair, please analyze why the buggy code contain errors and why the repaired code can function well and solve the given problem"
    
    if role == "inputter":
        return "".join(["Using the context provided, generate testing inputs satisfying the given constraints, along with a description. Take your time to analyze the task step-by-step, ",
                        "and ensure you cover all the bases. Your response format is like $$\n<input> @#& <description>\n$$. Each input-description pair must be enclosed with two dollar signs ($$). ",
                        "The generated inputs should not contain any omissions. No more any additional text!"])
    
    raise NotImplementedError

def get_retry_prompt(role, buggy_line_num=5):
    if role == "localizer":
        return "".join(["The code must be faulty so it delivers **UNEXPECTED or EMPTY or INCOMPLETE** outputs, as shown in failed test cases. Take a breath and analyze it once again, step by step. ",
                        f"Label NO MORE THAN {buggy_line_num} code lines directly causing bug(s) by adding a comment to the original given code, enclosed within THREE backticks (```). ",
                        "Then, provide a brief explanation of how tracking key parameter values helped in identifying the bugs, ENCLOSED within two dollar signs ($$)"])
    if role == "fixer":
        return "".join(["There must be some bugs so I provided the buggy lines and the **UNEXPECTED or EMPTY or INCOMPLETE** outputs in failed test cases. Take a breath and analyze it carefully, step by step. ",
                        "Please revisit the code and make minimal changes to correct it. Your answer should consist of the revised code, surrouned with THREE backticks (```), followed by a breif explaination enclosed within two dollar signs ($$)"])
    
    if role == "inputter":
        return "".join(["Your response is not in the desired format, or some of the generated inputs do not meet the constraits. Take a breath and analyze it once again, step by step. ",
                        "For each testing input, return the input content with a brief description of the reason of adopting this input, in the format of\n $$\n<input> @#& <description>\n$$. ",
                        "For multiple inputs, list each input-desciption pair in the same format. Each pair must be enclosed with dollar signs ($$). No more any additional text",])
    raise NotImplementedError

def get_backup_prompt(action):
    if action == "feedback":
        return "".join(["Take a breath and analyze the code and your previous repairing against the correspoding failed cases. Explictly track values of key parameters. "
                        "Return a new revised code surrouned with THREE backticks (```). Then, explain very briefly how tracking key parameter values helped in repairing the bugs, ",
                        "enclosed within two dollar signs ($$). No more additional text"])

    raise NotImplementedError
    
    
                   
                   
                   

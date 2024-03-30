import os
import json
import logging
import hashlib

def read_json(filepath):
    if os.path.exists(filepath):
        assert filepath.endswith('.json')
        with open(filepath, 'r') as f:
            return json.loads(f.read())
    else: 
        print("File path "+filepath+" not exists!")
        return
    
def json_pretty_dump(obj, filename):
    with open(filename, "w") as fw:
        json.dump(obj, fw, sort_keys=True, indent=4,
            separators=(",", ": "), ensure_ascii=False,)

def logging_activate(record_dir):
    os.makedirs(record_dir, exist_ok=True)
    log_file = os.path.join(record_dir, "running.log")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s P%(process)d %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )

def dump_exp(main_dir, params:dict):
    hash_id = hashlib.md5(str(sorted([(k, v) for k, v in params.items() if "limit" not in k])).encode("utf-8")).hexdigest()[0:8]
    record_dir = os.path.join(main_dir, "records", hash_id)
    os.makedirs(record_dir, exist_ok=True)

    json_pretty_dump(params, os.path.join(record_dir, "params.json"))
    logging_activate(record_dir)
    return record_dir, hash_id

def return_lines(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as rf:
            return rf.read().splitlines()
    return []

def write_line(file_path, line):
    with open(file_path, "a+") as wf:
        wf.write(line+"\n")

def cal_token(*args):
    lenth = 0
    for v in args:
        if isinstance(v, int):
            lenth += v * 2
        elif isinstance(v, str):
            lenth += len(v)
        elif isinstance(v, list) and isinstance(v[0], dict):
            lenth += sum([len(vd["content"]) for vd in v])
    return lenth // 2
        
        
    


        

    






import os
import yaml
import json
from subprocess import Popen, PIPE, STDOUT
import re
import time
from pprint import pprint
from script_utils import list_files_walk, check_tag_duplication
from functions.mitre_tags_check import main_mitre_tags_check
from functions.check_fields import main_check_fields

def main_validate(rule_id, flag, file_path):
        
    dirname = os.path.dirname(__file__)
    yaml_file = os.path.join(dirname, '../config.yaml')
    with open(yaml_file,'r') as f:
        config_data = yaml.safe_load(f,)
        repo_path = config_data['repo_path']
        rt_path = config_data['rt_path']
    output_flag = 0
    version_flag = 0
    file_path = file_path
    if flag!="None":
        if flag == "output":
            # print output
            output_flag = 1
        elif flag =="version":
            # change the version
            version_flag = 1
        else:
            print(f"\033[1minvalid flag - {flag}\033[00m")
            print(f"\033[1mavailable flags - output, version\033[00m\n")
    
    test_path = file_path.replace('rule.yaml','positiveTests/test.json')
    watchlist_path = os.path.join(repo_path,'watchlists')
    print(file_path)
    result = check_tag_duplication(file_path,config_data)
    if result[0] == "Error":
        print("\033[1;93mDuplicate tags found. Fixing it...\033[00m")
        with open(file_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        yaml_data["metadata"]["tags"] = result[1]
        with open(file_path,'w') as f:
            yaml.safe_dump(yaml_data,f)
    else:
        print(f"\n\033[1;92m{result[0]}\033[00m\n")
    if version_flag:
        print("\033[1;93mUpdating version...\033[00m")
        with open(file_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        yaml_data["version"] = int(time.time())
        with open(file_path,'w') as f:
            yaml.safe_dump(yaml_data,f)
    args = [rt_path, "--format", "RBC" ,"--rules",file_path, "--write-rules", file_path,"--events",test_path,"--watchlists",watchlist_path, "--output"]
    p = Popen(args,stdout=PIPE,stderr=STDOUT,universal_newlines=True)
    otpt = p.communicate()[0]
    p.kill()
    if version_flag:
        print(f"\n\033[1;92mVersion updated!\033[00m\n")
    if output_flag:
        print(f"{otpt}")
    pattern = re.compile(r"RESULT: Rule.*fired\s+\d+|s+times")
    try:
        matches = re.search(pattern,otpt)
    except Exception as e:
        print("Regex error: ",e)
    if matches:
        if flag != "output" : print(matches.group()+" times")
        print("\n\033[1;92mValidation checks passed\033[00m")
    else:
        print("\n\033[1;91mValidation checks failed\033[00m")
    main_mitre_tags_check(file_path)
    main_check_fields(file_path)
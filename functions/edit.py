import yaml
import os
import json
import sys
import time
from subprocess import Popen, PIPE
from script_utils import list_files_walk,file_operations, open_file_in_editor

def main_edit(rule_id,rule_type,file_path):

    while rule_id == "":
        print("Rule id not enetered!")
        rule_id = input("Please enter the rule id:\t")

    dirname = os.path.dirname(__file__)
    
    yaml_file = os.path.join(dirname, '../config.yaml')
    
    with open(yaml_file,'r') as f:
        df = yaml.safe_load(f,)
        rt_path = df['rt_path']
        directory_path = df['directory_path']
        
    if "2.2." in rule_id:
        rule_folder = os.path.join(dirname, f'{directory_path}/use_case_specific/{rule_id}')
    else:
        rule_folder = os.path.join(dirname, f'{directory_path}/one_stage_rules/{rule_id}')

    file_path = file_path
    if file_path:
        print("\033[92mFound\033[00m")
        print(file_path)
        open_file_in_editor(file_path)
    else:
        print("Oh new rule? All the best!")
        # if rule_id not in json_file.keys():
        d = {
            "id": rule_id,
            "version": int(time.time()),
            "name": "",
            "groupby": "",
            "require": 1,
            "within": "60s",
            "items": [],
            "metadata": {
                    "analytical": False,
                    "attacks": [],
                    "classification": "",
                    "confidence_id": 2,
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "kill_chain": [],
                    "recommended_action": [],
                    "recommended_query": [],
                    "risk_level_id": 2,
                    "severity_id": 3,
                    "silent": False,
                    "tags": [],
                    "threatType": ""
            }
        }

        # rule_type = rule_type
        if rule_type == "rf":
            d["metadata"]["analytical"] = True
        elif rule_type == "proxy":
            d["metadata"]["tags"] = ["6f05798d-781d-5142-b317-c3789cbecc73"]
            
        print(rule_id)
        file_operations(rule_folder)
        file_path = f'{rule_folder}/rule.yaml'
        with open(file_path,'w') as f:
            yaml.safe_dump(d,f)
        p = Popen([rt_path, "--format", "RBC", "--rules",file_path, "--write-rules",file_path],stdout=PIPE)
        p.wait()
        open_file_in_editor(file_path)
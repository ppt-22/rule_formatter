from subprocess import Popen, PIPE
from script_utils import list_files_walk, check_tag_duplication
from functionalities.check_fields import main_check_fields
import os
import yaml
import json


def main_fmt(file_path,rule_id=''):
    dirname = os.path.dirname(__file__)
        
    #yaml file with all the data
    yaml_file = os.path.join(dirname, '../config.yaml')

    with open(yaml_file,'r') as f:
        d = yaml.safe_load(f,)
        rt_path = d['rt_path']

    if rule_id != '':
        file_path = file_path
        print(rule_id)
        print(file_path)
        result = check_tag_duplication(file_path)
        if result[0] == "Error":
            print("\033[93mDuplicate tags found. Fixing it...\033[00m")
            with open(file_path, 'r') as f:
                yaml_data = yaml.safe_load(f)
            yaml_data["metadata"]["tags"] = result[1]
            with open(file_path,'w') as f:
                yaml.safe_dump(yaml_data,f)
        else:
            print("\033[92mNo duplicate tags found!\033[00m")
        p = Popen([rt_path, "--format", "RBC", "--rules", file_path, "--write-rules", file_path],stdout=PIPE)
        p.wait()
        main_check_fields(file_path)
    else:
        print("\033[91mFormat what? Give a valid rule id please...\033[00m")
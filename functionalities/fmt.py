from subprocess import Popen
from script_utils import list_files_walk,get_data, check_tag_duplication
import os
import yaml
import json


def main_fmt(rule_id=''):
    dirname = os.path.dirname(__file__)
        
    #yaml file with all the data
    yaml_file = os.path.join(dirname, '../config.yaml')
    json_file = os.path.join(dirname, '../rule_data.json')

    with open(yaml_file,'r') as f:
        d = yaml.safe_load(f,)
        rt_path = d['rt_path']


    with open(json_file,'r') as jf:
        rule_data = json.load(jf)
    
    if rule_id != '':
        try:
            file_path = rule_data[rule_id]
        except:
            s = get_data()
            file_path = s[rule_id]
        print(rule_id)
        print(file_path)
        result = check_tag_duplication(file_path)
        if result[0] == "Error":
            print("Duplicate tags found. Fixing it...")
            with open(file_path, 'r') as f:
                yaml_data = yaml.safe_load(f)
            yaml_data["metadata"]["tags"] = result[1]
            with open(file_path,'w') as f:
                yaml.safe_dump(yaml_data,f)
        else:
            print("No duplicate tags found!")
        p = Popen([rt_path, "--format", "RBC", "--rules", file_path, "--write-rules", file_path])
        p.wait()
    else:
        print("Format what? Give a rule id dude...")
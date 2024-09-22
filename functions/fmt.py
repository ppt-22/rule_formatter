from subprocess import Popen, PIPE
from script_utils import list_files_walk, check_tag_duplication, map_mitre
from functions.check_fields import main_check_fields
import os
import yaml
import json


def main_fmt(file_path,rule_id=''):
    dirname = os.path.dirname(__file__)
        
    #yaml file with all the data
    yaml_file = os.path.join(dirname, '../config.yaml')

    with open(yaml_file,'r') as f:
        config_data = yaml.safe_load(f,)
        rt_path = config_data['rt_path']

    if rule_id != '':
        file_path = file_path
        print("\n"+rule_id)
        print(file_path)
        result = check_tag_duplication(file_path,config_data)
        mitre_result = map_mitre(file_path,config_data)
        if result[0] == "Error":
            print("\n\033[93mDuplicate tags found. Fixing it...\033[00m")
        else:
            print("\n\033[1;92mNo duplicate tags found!\033[00m")
        with open(file_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        yaml_data["metadata"]["tags"] = result[1]
        yaml_data["metadata"]["attacks"] = mitre_result
        with open(file_path,'w') as f:
            yaml.safe_dump(yaml_data,f)
        p = Popen([rt_path, "--format", "RBC", "--rules", file_path, "--write-rules", file_path],stdout=PIPE,stderr=PIPE)
        otpt, err = p.communicate()
        p.kill()
        if err: print(err.decode())
        main_check_fields(file_path)
    else:
        print("\033[91mFormat what? Give a valid rule id please...\033[00m")
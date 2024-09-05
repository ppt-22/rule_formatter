import os
import yaml
import json
from subprocess import Popen
from script_utils import list_files_walk, get_data, check_tag_duplication
from functionalities.mitre_tags_check import main_mitre_tags_check

def main_validate(rule_id, flags):
        
    dirname = os.path.dirname(__file__)
    #yaml file with all the data
    yaml_file = os.path.join(dirname, '../config.yaml')
    json_file = os.path.join(dirname, '../rule_data.json')

    with open(yaml_file,'r') as f:
        d = yaml.safe_load(f,)
        directory_path = d['directory_path']
        rt_path = d['rt_path']
    
    with open(json_file,'r') as jf:
        rule_data = json.load(jf)
    

    try:
        file_path = rule_data[rule_id]
    except:
        s = get_data()
        file_path = s[rule_id]

    test_path = file_path.replace('rule.yaml','positiveTests/test.json')
    watchlist_path = directory_path.replace('rules/one_stage_rules/','watchlists')
    print(file_path)
    # flags = flags.strip(" ")
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
    args = [rt_path, "--format", "RBC" ,"--rules",file_path, "--write-rules", file_path,"--events",test_path,"--watchlists",watchlist_path, "--output"]
    # args.extend(flags)
    # print(args)
    p = Popen(args)
    p.wait()
    main_mitre_tags_check(file_path)
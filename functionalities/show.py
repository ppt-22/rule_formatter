import yaml
import sys
import os
import json
from script_utils import list_files_walk,print_yaml_in_color,get_data


def main_show(rule_id):
    dirname = os.path.dirname(__file__)
        
    #yaml file with all the data
    # yaml_file = os.path.join(dirname, '../config.yaml')
    json_file = os.path.join(dirname, '../rule_data.json')

    with open(json_file,'r') as jf:
        rule_data = json.load(jf)
    
    try:
        file_path = rule_data[rule_id]
    except:
        s = get_data()
        file_path = s[rule_id]

    print(file_path)
    print("-"*30)
    print_yaml_in_color(file_path)
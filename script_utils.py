import os
import yaml
import subprocess
import json
import math
import sys
from pygments import highlight
from pygments.lexers import YamlLexer
from pygments.formatters import TerminalFormatter
from datetime import datetime
from collections import Counter
import re
from script_utils import *

def check_version_update():
    dirname = os.path.dirname(__file__)
    r_0 = subprocess.run(["git","checkout","main"],cwd=dirname,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    r = subprocess.run(["git","status"],cwd=dirname,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.stderr.decode():
        print("Something went wrong")
    if "Your branch is behind 'origin/main' by " in r.stdout.decode():
        print("New version available. Please update")

def get_all_fields(dictionary,keys=[]):
    try:
        for key, value in dictionary.items():
            if type(value) is dict:           
                get_all_fields(value)
            if type(value) is list:  
                for i in value:        
                    get_all_fields(i)
                keys.append(key)
            else:
                keys.append(key)
    except:
        pass
    return keys

def get_duplicate_id(rule_list):
    d = Counter(rule_list)    
    new_list = list([item for item in d if d[item]>1])
    return new_list

def get_file_path(rule_id):
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, 'config.yaml')
    with open(config_file,'r') as file:
        config_data = yaml.safe_load(file,)
        directory_path = config_data["directory_path"]
    ace_files = list_files_walk(directory_path)
    return_code = 0
    rs = []
    for i in ace_files:
        pattern = re.compile(r"(\d\.\d\.\d+[\/|\\])")
        matches = list(set(re.findall(pattern,i)))
        if matches:
            if "\\" in matches[0]:
                matched_rule_id = matches[0].replace(r"\\","")
            if "/" in matches[0]:
                matched_rule_id = matches[0].replace("/","")
            rs.append(matched_rule_id)
            if matched_rule_id == rule_id:
                file_path = i
                return_code = 1
    if len(rs) != len(list(set(rs))):
        print("\033[1;91mDuplicate rule id found\033[00m")
        print(get_duplicate_id(rs))
        # exit(0)
    if return_code == 0:
        file_path = ""    
    return file_path,return_code

def check_tag_duplication(file_path):
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, 'config.yaml')
    with open(config_file,'r') as file:
        config_data = yaml.safe_load(file,)
        repo_path = config_data["repo_path"]
    with open(file_path, 'r') as f:
        yaml_data = yaml.safe_load(f)
    try:
        tags = yaml_data["metadata"].get("tags",[])
    except:
        print("\n\033[1;91mMetadata seems to be empty..\033[00m")
        exit(0)
    if len(tags) == len(list(set(tags))):
       return ["No duplication of tags!",tags]
    else:
       return ["Error",list(set(tags))]

# def check_last_update():
#     dirname = os.path.dirname(__file__)
#     config_file = os.path.join(dirname, 'config.yaml')

#     with open(config_file,'r') as file:
#         config_data = yaml.safe_load(file,)
#         timestamp = config_data["timestamp"]
#         repo_path = config_data["repo_path"]

#     current_time = datetime.now()
#     b = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second)

#     last_check = timestamp.split(" ")
#     a = datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]), int(last_check[3]), int(last_check[4]), int(last_check[5]))

#     diff = b-a
#     hours = diff.total_seconds()/3600
#     print("\033[90mlast update: ",math.ceil(hours*100)/100,"hours ago\033[00m")
#     if hours > 72:
#       subprocess.run(["git", "checkout", "main"], cwd=repo_path)
#       subprocess.run(["git", "pull"], cwd=repo_path)
#       with open(config_file,'w') as file:
#         config_data['timestamp'] = f"{current_time.year} {current_time.month} {current_time.day} {current_time.hour} {current_time.minute} {current_time.second}"
#         new_data = config_data
#         yaml.dump(new_data,file,sort_keys=False)
      


def list_files_walk(start_path='.'):
    list_files = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if ".yaml" in file:
                list_files.append(os.path.join(root, file))
    return list_files

def print_yaml_in_color(yaml_file):
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    colored_yaml = highlight(yaml.dump(yaml_data, default_flow_style=False,sort_keys=False), YamlLexer(), TerminalFormatter())
    print(colored_yaml)

def file_operations(rule_folder):
    create_dir_command = f"mkdir {rule_folder}"
    create_file_command = f"touch {rule_folder}/rule.yaml"
    test_folder = f"mkdir {rule_folder}/positiveTests"
    test_file = f"touch {rule_folder}/positiveTests/test.json"
    process = subprocess.Popen(create_dir_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(create_file_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(test_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(test_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

def open_file_in_editor(file_path):
    p_c = subprocess.Popen(["code", file_path])
    p_c.wait()
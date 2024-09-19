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
    r_0 = subprocess.run(["git","checkout","main"],cwd=dirname,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    r = subprocess.run(["git","status"],cwd=dirname,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    r_otpt, r_err = r.communicate()
    if r_err.decode():
        print("Something went wrong")
    if "Your branch is behind 'origin/main' by " in r_otpt.decode():
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
        if type(tags) != list:
            tags = [tags]
    except:
        print("\n\033[1;91mMetadata seems to be empty..\033[00m")
        exit(0)

    #json file with tag data
    tag_file = os.path.join(repo_path, 'config/tag_ids.json')

    with open(tag_file) as jf:
        tags_data = json.load(jf)

    new_tags = []
    flag = 0
    left_overs = []
    for i in tags:
        if i in tags_data.values():
            new_tags.append(i)
        elif i in "  ".join(tags_data.keys()).lower():
            flag = 1
            for j in tags_data.keys():
                if i.lower() in j.lower():
                    new_tags.append(tags_data[j])
                    # print(i)
        else:
            left_overs.append(i)
    if left_overs:
        print(f"\033[91mTags not found: {left_overs}\033[00m")
    if len(new_tags) == len(list(set(new_tags))):
       return ["No duplication of tags!",new_tags]
    else:
       return ["Error",list(set(new_tags))]

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
    try:
        p_c = subprocess.Popen(["code", file_path])
        p_c.wait()
    except:
        print("\n\033[1;30mSomething went wrong. Couldn't open the file. But the file is created\033[00M")
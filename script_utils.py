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
from script_utils import *

def check_tag_duplication(file_path):
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, 'config.yaml')
    with open(config_file,'r') as file:
        config_data = yaml.safe_load(file,)
        repo_path = config_data["repo_path"]
    with open(file_path, 'r') as f:
        yaml_data = yaml.safe_load(f)
    tags = yaml_data["metadata"].get("tags")
    if len(tags) == len(list(set(tags))):
       return ["No duplication of tags!",tags]
    else:
       return ["Error",list(set(tags))]

def get_data():
    rule_ids = []
    list_files = []
    json_data = {}
    dirname = os.path.dirname(__file__)
    json_file = os.path.join(dirname, 'rule_data.json')
    config_file = os.path.join(dirname, 'config.yaml')

    with open(config_file,'r') as file:
        config_data = yaml.safe_load(file,)
        current_time = datetime.now()
        direc_path = config_data["directory_path"]
    with open(config_file,'w') as file:
        config_data['timestamp'] = f"{current_time.year} {current_time.month} {current_time.day} {current_time.hour} {current_time.minute} {current_time.second}"
        yaml.dump(config_data,file,sort_keys=False)
    
    list_files = list_files_walk(direc_path)

    for yaml_file in list_files:
      with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
        rule_id = yaml_data.get("id")
        if rule_id not in rule_ids:
            json_data[yaml_data.get("id")] = yaml_file
        else:
           print(f"DUPLICATE RULE ID ({rule_id}) FOUND!")
           sys.exit(1)
        rule_ids.append(rule_id)

    out_file = open(json_file, "w")
    json.dump(json_data, out_file, indent = 4)
    out_file.close()
    return json_data

def check_last_update():
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, 'config.yaml')

    with open(config_file,'r') as file:
        config_data = yaml.safe_load(file,)
        timestamp = config_data["timestamp"]
        repo_path = config_data["repo_path"]

    current_time = datetime.now()
    b = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second)

    last_check = timestamp.split(" ")
    a = datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]), int(last_check[3]), int(last_check[4]), int(last_check[5]))

    diff = b-a
    hours = diff.total_seconds()/3600
    print("last update: ",math.ceil(hours*100)/100,"hours ago")
    if hours > 24:
      subprocess.run(["git", "checkout", "main"], cwd=repo_path)
      subprocess.run(["git", "pull"], cwd=repo_path)
      print("Updating rule data file")
      get_data()


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

  colored_yaml = highlight(yaml.dump(yaml_data, default_flow_style=False), YamlLexer(), TerminalFormatter())
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
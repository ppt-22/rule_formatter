import yaml
import sys
import os
import json
from script_utils import list_files_walk,print_yaml_in_color


def main_show(rule_id,file_path):
    dirname = os.path.dirname(__file__)   
    file_path = file_path
    print(file_path)
    print("-"*30)
    print_yaml_in_color(file_path)
import os
import yaml
import json
import sys


def main_mitre_tags_check(file_path):
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, '../config.yaml')
    with open(config_file,'r') as file:
        config_data = yaml.safe_load(file,)
        repo_path = config_data["repo_path"]
    mitre_file = os.path.join(repo_path, 'config/mitre_data.json')
    with open(mitre_file) as mf:
        mitre_data = json.load(mf)
    with open(file_path) as rf:
        rule_file = yaml.safe_load(rf,)
    rule_id = rule_file["id"]
    mitre_in_rule =  rule_file["metadata"]["attacks"]
    for attack in mitre_in_rule:
        tech_id = attack["technique"]["uid"]
        tac_fin = []
        for i in attack["tactics"]:
            tac_data = {
                "name": i["name"],
                "id": i["uid"]
            }
            tac_fin.append(tac_data)
        if tech_id in mitre_data.keys():
            if attack["technique"]["name"] != mitre_data[tech_id]["name"]:
                print(f"\033[91m[{rule_id}][{tech_id}] mitre technique name does not match\033[00m")
                sys.exit(1)
            if attack["version"] != str(mitre_data[tech_id]["version"]):
                print(f"\033[91m[{rule_id}][{tech_id}] mitre technique version does not match\033[00m")
                sys.exit(1)
            if mitre_data[tech_id]["tactics"] != tac_fin:
                print(f"\033[91m[{rule_id}][{tech_id}] mitre tactic does not match\033[00m")
                sys.exit(1)
        else:
            print(f"\033[91m{tech_id} not found in mitre data\033[00m")
    tags_file = os.path.join(repo_path, 'config/tag_ids.json')
    with open(tags_file) as tf:
        tags_orig = json.load(tf)
    tag_ids = []
    for k, v in tags_orig.items():
        tag_ids.append(v)
    if "tags" in rule_file["metadata"].keys():
        tag_list = rule_file["metadata"]["tags"]
        for tag in tag_list:
            if tag not in tag_ids:
                print(f"\033[91mTag {tag} do not exist. Exiting.\033[00m")
                sys.exit(1)
    print("\n\033[1;92mMitre and tags check passed!! Noice!\033[00m")

import subprocess
import yaml
import json
import os
import sys
import shutil
import pandas as pd
import yaml


dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, "../config.yaml")
convert_file = os.path.join(dirname,"translate_rule.py")

with open(config_file) as cf:
     config_data = yaml.safe_load(cf,)

rule_ids = sys.argv[1:]
print("\nGiven rule ids",rule_ids)
remaining_rule_ids = rule_ids[:]

#Get the list of all files and directories
rule_tester_path = config_data["rt_path"]
xdr_repo_path = config_data["repo_path"]
try:
    tap_path = config_data["tap_path"]
except:
    print("\nTap path is not present in the config file")
    tap_path = input("\nEnter tap path:\t")
    config_data["tap_path"] = tap_path
    with open(config_file,"w") as cf:
        yaml.safe_dump(config_data,cf)

prod_path = os.path.join(config_data["tap_path"],"rules/production")
dir_list = os.listdir(prod_path)

rule_data = []

for i in dir_list:
        if '.json' in i:
                with open(f'{prod_path}/{i}', 'r') as f:
                        # data = yaml.load(f, Loader=yaml.SafeLoader)
                        data = json.load(f,)
                        if data.get("id") in rule_ids:
                            remaining_rule_ids.remove(data.get("id"))
                            rule_data.append([data.get("id"),i])

def file_operations(r):
    create_dir_command = f"mkdir {xdr_repo_path}/rules/one_stage_rules/{r[0]}"
    create_file_command = f"touch {xdr_repo_path}/rules/one_stage_rules/{r[0]}/rule.yaml"
    test_folder = f"mkdir {xdr_repo_path}/rules/one_stage_rules/{r[0]}/positiveTests"
    test_file = f"touch {xdr_repo_path}/rules/one_stage_rules/{r[0]}/positiveTests/test.json"
    process = subprocess.Popen(create_dir_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(create_file_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(test_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(test_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    shutil.copy(f'{tap_path}/rules/tests/{r[0]}.json', test_file.replace("touch ",""))

    if os.path.isfile(f"{tap_path}/rules/tests/negative/{r[0]}.json"):
        n_test_folder = f"mkdir {xdr_repo_path}/rules/one_stage_rules/{r[0]}/negativeTests"
        n_test_file = f"touch {xdr_repo_path}/rules/one_stage_rules/{r[0]}/negativeTests/test.json"
        process = subprocess.Popen(n_test_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        process = subprocess.Popen(n_test_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()        
        shutil.copy(f'{tap_path}/rules/tests/negative/{r[0]}.json', n_test_file.replace("touch ",""))


for r in rule_data:

    file_operations(r)
    # Your long shell command
    rule_json_path = f"{prod_path}/{r[1]}"
    ace_path = f"{xdr_repo_path}/rules/one_stage_rules/{r[0]}/rule.yaml"
    command = f"python3 {convert_file} -v -o translate -m {xdr_repo_path}/config/mitre_data.json -r {rule_json_path} --out-file {ace_path} --ruletester {rule_tester_path}"
    # Run the command with Popen
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

    # Capture standard output and standard error (optional)
    output, error = process.communicate()

    # Check return code (optional)
    if process.returncode == 0:
        print("Command successful! Rule: ",r)
    else:
        print(f"Command failed with error code: {process.returncode}")
        # Print error output if needed
        print(f"Error: {error.decode()}")

print("\nRemaining not-converted rule ids",remaining_rule_ids)
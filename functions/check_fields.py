import yaml
import os
from script_utils import get_all_fields

def main_check_fields(file_path):

    issues = {}

    with open(file_path,"r") as rf:
        rule = yaml.safe_load(rf,)
    try:
        r_fields = get_all_fields(rule)
        rq = rule["metadata"].get("recommended_query")
    except:
        print("\n\033[1;91mMetadata section appears to be empty. Please check\033[00m")
        exit(0)
    
    dirname = os.path.dirname(__file__)
    yaml_file = os.path.join(dirname, '../maps/missing_fields.yaml')
    gi_yaml_file = os.path.join(dirname, '../maps/rq_class.yaml')
    
    with open(yaml_file,"r") as f:
        fields_messages = yaml.safe_load(f,)
        fields = list(fields_messages.keys())
    with open(gi_yaml_file,"r") as yf:
        gi_data = yaml.safe_load(yf,).get('MIN_GI_MAP')

    # Fields check
    leftover_fields = (list(set(fields)-set(r_fields)))
    if leftover_fields:
        fields = []
        for i in leftover_fields:
            fields.append(f"\t\033[1m{i}\033[00m: {fields_messages[i]}")
        issues["fields"] = fields
    # GI check
    queries = []
    for dic in rule["items"]:
        for val in dic:
            if val == "match": queries.append(dic[val])

    guid = []
    for term,gi_ids in gi_data.items():
        for q in queries:
            if term in q:
                for gi in gi_ids:
                    if gi not in rq:
                        guid.append(f'\tTerm "{term}" found in rule but recommended query (guided investigation) id not found: {gi}')
    if guid:
        issues["gi"] = guid

    if issues:
        print("\n\033[38:5:208msuggestions:\033[00m")
        for i in issues.get("fields",[]):
            print(i)
        print("")
        for i in issues.get("gi",[]):
            print(i)
        

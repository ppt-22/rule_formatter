import tempfile
import json
import yaml
import os
from subprocess import Popen, PIPE

def main_convert():
    dirname = os.path.dirname(__file__)
        
    #yaml file with all the data
    yaml_file = os.path.join(dirname, '../config.yaml')

    with open(yaml_file,'r') as f:
        config_data = yaml.safe_load(f,)
        rt_path = config_data['rt_path']


    helix_query = input("\nEnter the helix query:     ")

    # create the temporary json file
    temp = tempfile.NamedTemporaryFile(suffix='.json',mode='w+')
    d = {"id": "1.1.9999", "message": "test", "eventsThreshold": 1, "secondsThreshold": "60s", "search": helix_query}
    json.dump(d, temp)
    temp.seek(0)

    # create the temporary yaml file
    temp_yaml = tempfile.NamedTemporaryFile(suffix='.yaml',mode='w+')
    temp_yaml.seek(0)

    p = Popen([rt_path, "--format", "helix", "--rules",f"{temp.name}" , "--write-rules", f"{temp_yaml.name}"],stdout=PIPE,stderr=PIPE)
    otpt, err = p.communicate()
    p.kill()
    ace_query = yaml.safe_load(temp_yaml,)["items"][0]["match"]
    print("")
    print(f"\n\n\nAce query:\n\n{ace_query} \n\n")

    temp.close()
    temp_yaml.close()
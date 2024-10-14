import tempfile
import json
import yaml
from subprocess import Popen

def main_convert():
    helix_query = input("\nEnter the helix query:     ")

    # create the temporary json file
    temp = tempfile.NamedTemporaryFile(suffix='.json',mode='w+')
    d = {"id": "1.1.9999", "message": "test", "eventsThreshold": 1, "secondsThreshold": "60s", "search": helix_query}
    json.dump(d, temp)
    temp.seek(0)

    # create the temporary yaml file
    temp_yaml = tempfile.NamedTemporaryFile(suffix='.yaml',mode='w+')
    temp_yaml.seek(0)

    p = Popen([f"/home/pavan_pothams/projects/ruletest", "--format", "helix", "--rules",f"{temp.name}" , "--write-rules", f"{temp_yaml.name}"])
    p.wait()
    p.kill()
    ace_query = yaml.safe_load(temp_yaml,)["items"][0]["match"]
    print("")
    print(f"\n\n\nAce query:\n\n{ace_query} \n\n")

    temp.close()
    temp_yaml.close()
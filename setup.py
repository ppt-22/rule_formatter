import yaml
import os
import subprocess
from datetime import datetime

dirname = os.path.dirname(__file__)
main_file = os.path.join(dirname, 'main.py')

def source_bashrc():
    if os.environ.get("SHELL") == "/bin/bash":
        subprocess.run(["bash", "source ~/.bashrc"], shell=True, check=True)
        print()
    elif os.environ.get("SHELL") == "/bin/zsh":
        subprocess.run(["zsh","source ~/.bashrc"], shell=True, check=True)
    else:
        print("Error: Unsupported shell")

q_1 = 'p'

while True:
    q_1 = input("This your first time? [y/n] ")
    if q_1.lower()=='y':
        print("\nWelcome! Creating a config.yaml!\n")
        with open('config.yaml','w') as fp:
            pass
        break
    elif q_1.lower()=='n':
        print("Alright, then I'm assuming you already have config.yaml setup already")
        break
    else:
        print("wrong choice. You must pick from 'y' or 'n'")

ace_path = input("Enter path to your ace rules repository :    ")
rt_path = input("Enter path to your ruletester :    ")

yaml_file = os.path.join(dirname, 'config.yaml')
directory_path = os.path.join(ace_path, 'rules/')

shell_path = os.environ.get("SHELL")
print(shell_path)
shell = ""
if shell_path:
    if "bash" in shell_path:
        shell = "bashrc"
    elif "zsh" in shell_path:
        shell = "zshrc"
    else:
        shell = "bashrc"

r = subprocess.run(["which","python"])
if r.returncode==0:
    python_v = "python"
else:
    r = subprocess.run(["which","python3"])
    if r.returncode==0:
        python_v = "python3"
    else:
        print("ERROR")
        exit(0)

current_time = datetime.now()
config_data = {
    'repo_path' : ace_path,
    'directory_path' : directory_path,
    'rt_path' : rt_path,
    'python_v': python_v,
    # 'timestamp': f"{current_time.year} {current_time.month} {current_time.day} {current_time.hour} {current_time.minute} {current_time.second}"
}
with open(yaml_file,'w') as file:
    new_data = config_data
    yaml.dump(new_data,file,sort_keys=False)

print("\nconfig.yaml: I'M ALIVEEEE!\n")

if q_1=='y':

    q_2 = 'p'

    while True:
        q_2 = input("The next step would be setting an alias by writing it to .bashrc file and sourcing it. Do you wish to proceed? [y/n] ")
        if q_2.lower()=='y':
            shortcut = input("Enter your custom alias or hit enter for default value 'ace_rk':  ")
            if shortcut == '':
                shortcut = "ace_rk"
            print("Setting alias for you...")
            command = f"""echo "alias {shortcut}='{python_v} {main_file}'" >> ~/.{shell}"""
            process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait()
            process.kill()
            print("Done!")
            if q_1=='y':
                print("\nHow to use:")
                
                print("-> use edit to edit a rule or create a new rule with template")
                print("-> use fmt to format a rule")
                print("-> use show to print out a rule on terminal")
                print("-> use validate to validate a rule")
                print("-> use list to list out the functions offered by this tool")
            else:
                print("\nTips:")
                print("-> use -h or --help for help")
            source_bashrc()
            break
        elif q_2.lower()=='n':
            print(f"\n{main_file} is the path to the main file. Run this file to use this tool.")
            break
        else:
            print("wrong choice. You must pick from 'y' or 'n'")




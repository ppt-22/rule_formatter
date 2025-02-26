import argparse
import os
import yaml
import click
from subprocess import Popen,PIPE,STDOUT
from pprint import pprint
from argparse import RawTextHelpFormatter
from script_utils import get_file_path, check_version_update
from functions.fmt import main_fmt
from functions.show import main_show
from functions.edit import main_edit
from functions.validate import main_validate
from functions.update import main_update
from functions.convert import main_convert
from functions.translate import main_translate


def main(args):
    option = args.option
    rule_id = ""
    file_path = ""
    if args.rule:
        rule_id = args.rule
        # print(rule_id)
        # ans = input("proceed? y/n")
        id_flag = False
        while(not id_flag):
            if len(rule_id) < 7:
                print("\033[93mEnter complete id please\033[00m")
                rule_id = input("Enter correct rule id:     ")    
            else:
                id_flag = True
        file_path = get_file_path(rule_id)
        if file_path[1] == 0 and option != "edit" and option != "translate":
            print("\033[91mErm..not found\033[00m")
            exit(0)
        else:
            file_path = file_path[0]
    if option == "fmt":
        check_version_update()
        print(f"\n\033[96;1mFormatting rule {rule_id}\033[00m")
        # check_last_update()
        main_fmt(file_path,rule_id)
    elif option == "show":
        check_version_update()
        print(f"\n\033[96;1mDisplaying rule {rule_id}\033[00m")
        # check_last_update()
        main_show(rule_id,file_path)
    elif option == "validate":
        check_version_update()
        print(f"\n\033[96;1mValidating rule {rule_id}\033[00m")
        # check_last_update()
        flag = f'{args.type}'
        main_validate(rule_id,flag,file_path)
    elif option == "translate":
        check_version_update()
        ids = rule_id.split(" ")
        rem_ids = ids.copy()
        for i in ids:
            print(f"\n\033[96;1mTranslating rule {i} to ace format\033[00m")
            main_translate(i)
            rem_ids.remove(i)
        print("Rem ids: ",rem_ids)
    elif option == "edit":
        check_version_update()
        print(f"\n\033[96;1mEditing rule {rule_id}\033[00m")
        rule_type = f'{args.type}'
        main_edit(rule_id,rule_type,file_path)
    elif option == "convert":
        main_convert()
    elif option == "update":
        print(f"\n\033[96;1mChecking for updates...\033[00m")
        main_update()
    elif option == "renew":
        print(f"\n\033[96;1mWant to update the config file?\033[00m")
        dirname = os.path.dirname(__file__)
        yaml_file = os.path.join(dirname, 'config.yaml')
        with open(yaml_file,"r") as cf:
            config_data = yaml.safe_load(cf,)
        config_data["repo_path"] = click.prompt("Enter the new xdr_ace folder path or press enter if you want it unchanged: ",type=str,default=config_data.get("repo_path",""))
        config_data["directory_path"] = os.path.join(config_data["repo_path"], 'rules/')
        config_data["rt_path"] = click.prompt("Enter the new ruletest path or press enter if you want it unchanged: ",type=str,default=config_data.get("rt_path",""))
        config_data["tap_path"] = click.prompt("Enter the new tap folder path or press enter if you want it unchanged: ",type=str,default=config_data.get("tap_path",""))
        with open(yaml_file,'w') as file:
            new_data = config_data
            yaml.dump(new_data,file,sort_keys=False)
        print("\n\n")
        pprint(config_data)
    elif option == "list":
        check_version_update()
        print("""
    -> \033[96;4;1medit\033[00m
        This command can be used when the user wishes to edit an already existing rule or to create a new rule file. 
        The actions can be distinguished by the rule id passed in the command. When passed the rule id of an already exisiting rule, 
        the rule file will be opened but when the rule id does not exist, a new folder for the rule will be created with a skeleton 
        where the user can fill in the details.
        Additonally, when creating a new rule, an additonal argument, either 'rf' or 'proxy', can be passed respectively if the user 
        wishes to create a new rf rule or proxy rule. This is not a mandatory argument. If left blank, a regular rule will be created.
        Usage:
          For creating a regular rule - ace_rk edit 1.1.8999 (here 1.1.8999 is the id of the new rule the user wishes to create)
          For creating a proxy rule - ace_rk edit 1.1.8999 rf (here 1.1.8999 is the id of the new rule the user wishes to create)
          For creating an rf rule - ace_rk edit 1.1.8999 proxy(here 1.1.8999 is the id of the new rule the user wishes to create)
        
          For editing an exiting rule - ace_rk edit 1.1.4249 (here 1.1.4249 is the id of an already exisitng rule)
    -> \033[96;4;1fmt\033[00m
        This command formats the rule in a rather syntactical manner that is to be followed in an ace rule. While it tests, it also 
        checks for duplication in the tags, missing non-mandatory fields and missing recommended queries (guided investigations) in 
        the rule and suggests the same.
        Usage:
          ace_rk fmt 1.1.4249
    -> \033[96;4;1mshow\033[00m
        This command displays a rule on the terminal when a rule id is passed to the command.
        Usage:
          ace_rk show 1.1.4249
    -> \033[96;4;1mvalidate\033[00m
        This command tests the rule whose rule id has been passed as an argument in the command against the test cases from the test.json file. 
        While it tests, it also validates the mitre data, the tags in the rule, non-mandatory fields and recommended queries (guided investigations), 
        checking for errors in the mitre data and duplication in the tags and suggesting over the missing non-mandatory fields and recommended queries.
        Usage:
          ace_rk validate 1.1.4249
    -> \033[96;4;1mupdate\033[00m
        This command updates the rule_formatter tool.
        Usage:
          ace_rk update
    -> \033[96;4;1mconvert\033[00m
        This command helps in converting helix query to ace query.
        Usage:
          ace_rk convert
    -> \033[96;4;1mrenew\033[00m
        This command helps in updating the paths of xdr repository or ruletest path.
        Usage:
          ace_rk renew
    -> \033[96;4;1mlist\033[00m
        This command lists out the functions the tool offers.
        Usage:
          ace_rk list
""")
    else:
        print(f"\n\033[91;1mInvalid option - '{option}'\033[00m")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rule Library",formatter_class=RawTextHelpFormatter,epilog="""How to use:
     -> \033[96;4;1medit\033[00m
         This command can be used when the user wishes to edit an already existing rule or to create a new rule file. 
         The actions can be distinguished by the rule id passed in the command. When passed the rule id of an already exisiting rule, 
         the rule file will be opened but when the rule id does not exist, a new folder for the rule will be created with a skeleton 
         where the user can fill in the details.
         Additonally, when creating a new rule, an additonal argument, either 'rf' or 'proxy', can be passed respectively if the user 
         wishes to create a new rf rule or proxy rule. This is not a mandatory argument. If left blank, a regular rule will be created.
         Usage:
           For creating a regular rule - ace_rk edit 1.1.8999 (here 1.1.8999 is the id of the new rule the user wishes to create)
           For creating a proxy rule - ace_rk edit 1.1.8999 rf (here 1.1.8999 is the id of the new rule the user wishes to create)
           For creating an rf rule - ace_rk edit 1.1.8999 proxy(here 1.1.8999 is the id of the new rule the user wishes to create)
          
           For editing an exiting rule - ace_rk edit 1.1.4249 (here 1.1.4249 is the id of an already exisitng rule)
     -> \033[96;4;1mfmt\033[00m
         This command formats the rule in a rather syntactical manner that is to be followed in an ace rule. While it tests, it also 
         checks for duplication in the tags, missing non-mandatory fields and missing recommended queries (guided investigations) in 
         the rule and suggests the same.
         Usage:
           ace_rk fmt 1.1.4249
     -> \033[96;4;1mshow\033[00m
         This command displays a rule on the terminal when a rule id is passed to the command.
         Usage:
           ace_rk show 1.1.4249
     -> \033[96;4;1mvalidate\033[00m
         This command tests the rule whose rule id has been passed as an argument in the command against the test cases from the test.json file. 
         While it tests, it also validates the mitre data, the tags in the rule, non-mandatory fields and recommended queries (guided investigations), 
         checking for errors in the mitre data and duplication in the tags and suggesting over the missing non-mandatory fields and recommended queries.
         Usage:
           ace_rk validate 1.1.4249
     -> \033[96;4;1mupdate\033[00m
         This command updates the rule_formatter tool.
         Usage:
           ace_rk update
     -> \033[96;4;1mlist\033[00m
         This command lists out the functions the tool offers.
         Usage:
           ace_rk list
                                          """)
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose output")
    parser.add_argument("option", help="Represents the function you want to perform. Values: edit, fmt, show, validate, update, list", nargs="?")
    parser.add_argument("rule", help="A positional argument. Represents the rule id on which the function needs to be performed", nargs="?")
    parser.add_argument("type", type=str, help="A positional argument. Represents the type of rule you want to create with 'edit' function. available options: rf, proxy. default is atomic", nargs="?")
    args = parser.parse_args()
    main(args)
from subprocess import Popen
import os
import argparse
import yaml
import sys
from script_utils import list_files_walk,check_last_update,get_data
from functionalities.fmt import main_fmt
from functionalities.show import main_show
from functionalities.edit import main_edit
from functionalities.validate import main_validate

def main(args):
    # Specify the directory path you want to start from
    
    option = args.option
    rule_id = ''
    if args.rule:
        rule_id = args.rule if '1.1.' in args.rule or "2.1." in args.rule else f"1.1.{args.rule}"
    if option == "fmt":
        print(option)
        check_last_update()
        main_fmt(rule_id)
    if option == "show":
        print(option)
        check_last_update()
        main_show(rule_id)
    if option == "validate":
        print(option)
        check_last_update()
        flags = []
        main_validate(rule_id,flags)
    if option == "edit":
        rule_type = f'{args.type}'
        print(option)
        check_last_update()
        main_edit(rule_id,rule_type)
    if option == "update":
        get_data()
        check_last_update()
    if option == "list":
        print("""
                -> use edit to edit a rule or create a new rule with template
                -> use fmt to format a rule
                -> use show to print out a rule on terminal
                -> use validate to validate a rule
                -> use update to update the rule_data file manually
                -> use list to list out the functionalities offered by this tool 
""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rule Library\n")
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose output")
    parser.add_argument("option", help="Represents the function you want to perform. Values: edit, fmt, show, validate, update, list", nargs="?")
    parser.add_argument("rule", help="A positional argument. Represents the rule id on which the function needs to be performed", nargs="?")
    parser.add_argument("type", type=str, help="A positional argument. Represents the type of rule you want to create with 'edit' function. available options: rf, proxy. default is atomic", nargs="?")
    args = parser.parse_args()
    main(args)
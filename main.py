import argparse
from script_utils import get_file_path,check_last_update
from functions.fmt import main_fmt
from functions.show import main_show
from functions.edit import main_edit
from functions.validate import main_validate
from functions.update import main_update


def main(args):
    option = args.option
    rule_id = ""
    file_path = ""
    if args.rule:
        rule_id = args.rule
        id_flag = False
        while(not id_flag):
            if len(rule_id) < 7:
                print("\033[93mEnter complete id please\033[00m")
                rule_id = input("Enter correct rule id:     ")    
            else:
                id_flag = True
        file_path = get_file_path(rule_id)
        if file_path[1] == 0 and option != "edit":
            print("\033[91mErm..not found\033[00m")
            exit(0)
        else:
            file_path = file_path[0]
    if option == "fmt":
        print(f"\n\033[96;1mFormatting rule {rule_id}\033[00m")
        check_last_update()
        main_fmt(file_path,rule_id)
    if option == "show":
        print(f"\n\033[96;1mDisplaying rule {rule_id}\033[00m")
        check_last_update()
        main_show(rule_id,file_path)
    if option == "validate":
        print(f"\n\033[96;1mValidating rule {rule_id}\033[00m")
        check_last_update()
        flag = f'{args.type}'
        main_validate(rule_id,flag,file_path)
    if option == "edit":
        print(f"\n\033[96;1mEditing rule {rule_id}\033[00m")
        rule_type = f'{args.type}'
        check_last_update()
        main_edit(rule_id,rule_type,file_path)
    if option == "update":
        print(f"\n\033[96;1mChecking for updates...\033[00m")
        main_update()
    if option == "list":
        print("""
                -> use edit to edit a rule or create a new rule with template
                -> use fmt to format a rule
                -> use show to print out a rule on terminal
                -> use validate to validate a rule
                -> use update to update the tool
                -> use list to list out the functions offered by this tool 
                -> For detailed info read the README.md file
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
# rule_formatter
A basic python script to display (show), format (fmt), edit (edit) and validate (validate) ace rules.
A custom alias can be set if chosen while setting up the script, else default (ace_rk) value will be set.
The tool provides multiple functionalities which are mentioned below.

## show
This command displays a rule on the terminal when a rule id is passed to the command. 
Usage:
  `ace_rk show 1.1.4249`

## fmt
This command formats the rule in a rather syntactical manner that is to be followed in an ace rule.
Usage:
  `ace_rk fmt 1.1.4249`

## edit
This command can be used when the user wishes to edit an already existing rule or to create a new rule file. The actions can be distinguished by the rule id passed in the command. When passed the rule id of an already exisiting rule, the rule file will be opened but when the rule id does not exist, a new folder for the rule will be created with a skeleton where the user can fill in the details. 
Additonally, when creating a new rule, an additonal argument, either 'rf' or 'proxy', can be passed respectively if the user wishes to create a new rf rule or proxy rule. This is not a mandatory argument. If left blank, a regular rule will be created.
Usage:
  For creating a regular rule - `ace_rk edit 1.1.8999`       (here 1.1.8999 is the id of the new rule the user wishes to create)
  For creating a proxy rule   - `ace_rk edit 1.1.8999 rf`    (here 1.1.8999 is the id of the new rule the user wishes to create)
  For creating an rf rule     - `ace_rk edit 1.1.8999 proxy` (here 1.1.8999 is the id of the new rule the user wishes to create)

  For editing an exiting rule - `ace_rk edit 1.1.4249`       (here 1.1.4249 is the id of an already exisitng rule)

## update
This command updates the json rule data file from which the script fetches the rule file path whose id is passed in the argument.
Usage:
  `ace_rk update`

## list
This command lists the functionalities the script provides.
Usage:
  `ace_rk list`

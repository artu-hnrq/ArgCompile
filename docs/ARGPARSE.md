# Argparse

## ArgumentParser
* Package's main object, responsible by parse execution over an input string
* Accumulate arguments to customize parse process

### Arguments
* Name
* Positionality and/or optionality,
* Quantity 
* Predefined value
* Possible choices

* Description 

### Type
* Callable able to convert an input string into a python value

### Action
* Apply logic over converted input 
* Fulfill namespace

### Namespace
* DTO-like object that hold through fields parse results


## Parser process
parse_know_args:
* Identify input (default argv)
* Create Namespace
* Set default values in it

_parse_know_args:
** Map mutually exclusive arguments

* Identify input string patters: "AOOAOA"
  * Map positional pattern: "A"
  * Map optional (starts with prefix char) pattern: "O" 
    * Take care of short and long options, and possible abbreviations
    * Pick associated action
    * Split explicit value (usage of =)
  * register optional string indices

* Iterate over argument pattern
  * Alternating positional and optional consumption 
    - Consuming positionals:
      - Map each action to a regular expression based on number of args 
      - Slice off from the final of positionals action list, trying to find a (re) match with argument pattern
      - Apply actions to matched args, after converting them to associated type, cheking if result is valid choice
    - Consuming optionals:
      - Identify composition of multiple short options together
      - Identify provided concatenated value [ -Fvalue ]
      - Execute related actions, passing associated used option string and possible matched values
  * During the process:
    * Register unmatched arguments (extras)
    * Register seen actions ones (and those whose resultant value isn't the default)
    * Check for action's mutually exclusiveness
    
* By the end:
  * Check presence of all required actions and groups

# Uncover
* Just mutual-exclusiviness are treat
  * How about conditional requirement, 
* Multiple argument process

### Proposal
* Attributes - post process

### Other related packages

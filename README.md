# What is this?

py-ecm-validator is a Python 2.7 module used to validate Educational Concept Maps 
([Topic Maps](http://wandora.org)) in xtm format.

# Usage

## Installation

    pip -r requirements.txt
    python setup.py install
    
## Command line usage

**Example**:

``` 
    # No debugging
    python -m ecm_validator -f file.xtm
    
    
    # Validate file.xtm debugging the parser
    python -m ecm_validator -f file.xtm -d p
```

**Complete CLI commands**:  

```
    usage: Arguments for parser [-h] [-d DEBUG] -f FILE

    optional arguments:
    -h, --help            show this help message and exit
    -d DEBUG, --debug DEBUG
                        Debug flags, accepted in whatever order:'i' for input
                        debug;'l' for lexer debug; 'p' for parser debug;'o'
                        for output debug. Example '-d iplo', '-d olpi'.
    -f FILE, --file FILE  Input file
```

## Script usage

```python
from ecm_validator.xtm_parser import xml_parse
from ecm_validator.xtm_validator import validate_constraints

with open("file.xtm") as file_xtm:
    root = xml_parse(file_xtm)
    validate_constraints(root)
```

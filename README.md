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

## License

Copyright 2017 GrebeTeam

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Haifu
The haiku programming language (by David Morgan-Mar) interpreter. See the published 
[spec](https://www.dangermouse.net/esoteric/haifu.html) for full details.

## Setup

You need python3 and the `requirements.txt` installed to your environment.

Linux example (with apt):
```shell
sudo apt install python3 python3-venv
git clone https://github.com/haltosan/haifu.git
cd haifu
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## How to interpret programs
```shell
python3 haifu.py INPUT_FILE_NAME [DEBUG=0|1]
```

Ex: 
```shell
python3 haifu.py examples/hello_world.haifu 1
```

The program will output to stdout, the debug information will output to stderr. The debug argument (optional) needs to 
be '0' or '1'.

The `examples` directory has `*.haifu` files that contain valid haifu programs. The `examples/simplified` directory 
contains `*.txt` files that have simplified haifu programs. These aren't syntactically valid, but contain the same 
logic / opcodes of the language (between parser and interpreter layer).

## Spec clarification
The core source of truth is the spec published by David Morgan-Mar. The fallback source of truth is the interpreter 
itself. This section will attempt to provide an English description of choices the interpreter made in light of 
ambiguity in the core spec.

> When Celestial Bureaucrat Control words are interpreted, the Bureaucrat does not automatically ascend. Otherwise, the 
Bureaucrat will ascend after each word is interpreted.  
> Punctuation sits in its own rank in the Bureaucracy.    
> Words are split on ' ' or '\n'.  
> Variables with data of length 1 of type int become the single value. Longer variables will be lists.  
> Print commands (say, age) will only output single values.  
> When the Celestial Bureaucrat encounters a variable that contains a list of instructions, the Bureaucrat interprets 
the instructions as if it was a new program. The Bureaucrat will return up a Bureaucracy on the 'heaven' instruction. 
Variable values and side effects will carry through.  
> With the 'blossom' instruction, the jump value is the striving value that the Delegate observes.  
> Random integer values will be [0, 2^32].  
> Haiku stanzas are separated by a blank line. The final stanza doesn't need to be followed by a blank line.  
> Literals present in the program at parse time will be evaluated for balance. There must be an identical number of 
values that have Yin quality as Yang quality.  
> Numbers will only be in the english form (one) and not numerical form (1).
> Disallowed vulgar words can be found in `parse.py`. 


## Running the testsuite
The test suite is built for pytest. The test files live in the `test` directory. To run, activate the environment and 
run the pytest module from the main project directory:
```shell
source .venv/bin/activate
python3 -m pytest
```

To view coverage data, running the `test/coverage.sh` script (on platforms with bash) will generate an html coverage 
report.
```shell
cd test
chmod +x coverage.sh
./coverage.sh
# to view report
open ../htmlcov/index.html
```

## Interacting with the libraries
The remaining python files can be imported to get lower level functionality:
- `haifu_common.py` is a set of common data structures
- `parse.py` is the parser layer (read file -> validate syntax -> create list of tokens)
- `interpret.py` is the interpreter layer (read list of tokens -> perform program actions)

See the documentation in the files themselves (docstrings, type hints on the signatures, etc.) and testsuite for usage 
details.

## Contributing
The style guide is still a work in progress. Once there's a v1 release, the repo will be open for PR's.
# Style Guide
Commits/files/issues/pull requests in this repo MUST follow this style guide.

## Code
Code is functional python.  
Code MUST follow PEP 8.  

### In code docs
In code docs are comments, docstrings, and type hints inside code files.  
Type hints MUST use the typing library and builtin type hint system.  
Functions MUST have type hints on the signatures.  
Variables MAY have type hints.  
Docstrings MUST be in the reStructuredText (reST) format.  
Functions expected to be used outside its file MUST have docstrings.  
Other function MAY have docstrings.  


## Commits
Commits are git commits.  
Commits MUST make only one change.  
Commits MAY span multiple files, but the files MUST be related to the same change.  
Commit messages SHOULD be written as instructions. Ex: "Fix typo in variable name".  
Commits SHOULD pass the testsuite. Exceptions include testing driven development (contract test -> develop feature).  
Pull requests MUST pass the testsuite.  
Major releases MUST have a comprehensive test suite. This MUST include unit tests. This MAY include coverage tests.  
Branch names MUST contain the issue number and have a short description. Format: '{description}-{issue number}'.  

### Code commits
Code commits are commits focused on changing code.  
Bugfix commits SHOULD include the word 'bugfix' or 'fix'.  
Style commits SHOULD include the word 'style'.  

### Doc commits
Doc commits are commits focused on changing the english docs and the in code docs.  
Doc commits MUST be after the corresponding code change commits.  
Doc commits MUST start with the message 'DOCS - '.  


## Documentation
The english docs are documentation files written out in plain english not inside code files.  
The style guide MUST be RFC 2119 compliant.  
English docs SHOULD follow similar conventions as the README.  


## Issues
Issues are GitHub issues.  
Feature requests MUST start with 'Feature request - ' in the issue title.  
Bug issue titles MUST be focused on the issue behaviour. Ex: 'interpreter crashes on divide by 0' instead of 'fix the math'.  
Issues MUST be resolved with a pull request from a non-master branch to master.  
# When to make an Issue
Always. For every new feature and for every bug there should be a seperate issue.

# When to make a Branch
For every issue, there should be a branch

# Branching
Branching should be never be done directly off of master (besides the lone development branch)

# Pull Requests
+ Branches should merged into development via Pull-Requests.
+ Pull-Requests should always have at least one reviewer who will approve the work done

# Documentation/Formatting
## Functions
+ Explicitly stated types
  + All parameters must have types
  + All return types must be explicity stated
  + `def example(string:str) -> int`
+ Doc Strings: [Numpy style](https://numpydoc.readthedocs.io/en/latest/format.html)
  + **EXCEPTION**: Doc strings for functions exposed as commands should not document the ctx object.
    + This is because the doc string is sent to the user when they ask for "help" with that command.
## Style
+ Please follow these guidelines: [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008)

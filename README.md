pyfunc
======

Call python functions from your shell

### Install 

./install.sh

### Uninstall 

./uninstall.sh

### Examples

* For builtin functions - just call them without any module prefix. For others,
  prefix them by their module name.

    pyfunc -m range -a 1 5 2

    pyfunc -m string.upper -a test

* Arguments can also be read from standard input by providing '-' symbol

    echo 1 | pyfunc -m range -a - 5 2

* If the function takes only one argument (or others are optional),
  there is no need to give -a if you are feeding it from stdin

    echo TeSt | pyfunc -m string.swapcase

* Method signatures are assumed - if what you pass looks like an int - we wil
  convert it to int before passing it to the target function. However, if the
  user wants to explicitly specify method signature - he can do so. Apart from
  str/int - there is basic support to pass in other data types (list for now)

    pyfunc -m string.join -s list,str -a "Good news everyone" " burp "

    pyfunc -m sum -s list:int,str -a "1 2 3"

* pyfunc provides some basic utility functions which are present in pyfunc.utils

    pyfunc -m pyfunc.utils.json_flatten -a nested_json_file

* The right use case would be to create aliases out of commonly used functions
  and use them in your command pipelines:

    alias jsonflatten='pyfunc -m pyfunc.utils.json_flatten -a'
    alias strupper='pyfunc -m string.upper -a'

    cat test.json | jsonflatten | strupper

### What this module isn't

* Replacement for shell utilities - pyfunc's aim is to make your utility
  functions available on the command line.

### TODO

- Pip it
- Usage documentation
- Use docopt instead of argparse

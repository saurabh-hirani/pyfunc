pyfunc
======

Call python functions from your shell

### Install 

pip install pyfunc

### Examples

* For builtin functions - just call them without any module prefix. For others,
  prefix them by their module name.

```
  pyfunc -m range -a 1 5 2
  pyfunc -m string.upper -a test
  pyfunc -m string.replace -a 'analyze what' 'what' 'this'
```

* Arguments can also be read from standard input by providing '-' symbol

```
  echo 1 | pyfunc -m range -a - 5 2
```

* If the function takes only one argument (or others are optional),
  there is no need to give -a if you are feeding it from stdin

```
  echo TeSt | pyfunc -m string.swapcase
```

* Method signatures are assumed - if what you pass looks like an int - we wil
  convert it to int before passing it to the target function. However, if the
  user wants to explicitly specify method signature - he can do so. Apart from
  str/int - there is basic support to pass in other data types (list for now)

```
  pyfunc -m string.join -s list,str -a "Good news everyone" " burp "
  pyfunc -m sum -s list:int,str -a "1 2 3"
```

* For return values - you can print output in 3 ways:
  - shell (default) - print strings as they are, list and dicts by iterating
    over them
  - raw\_json
  - pretty\_json

```
  curl http://headers.jsontest.com/ 2>/dev/null | pyfunc -m pyfunc.utils.json_read -a -
  curl http://headers.jsontest.com/ 2>/dev/null | pyfunc -m pyfunc.utils.json_read -p raw_json -a -
  curl http://headers.jsontest.com/ 2>/dev/null | pyfunc -m pyfunc.utils.json_read -p shell -a -
```

* pyfunc provides some basic utility functions which are present in pyfunc.utils

```
  pyfunc -m pyfunc.utils.json_flatten -a nested_json_file
```

* The right use case would be to create aliases out of commonly used functions
  and use them in your command pipelines:

```
  alias jsonflatten='pyfunc -m pyfunc.utils.json_flatten -a'
  alias strupper='pyfunc -m string.upper -a'
  curl http://pastebin.com/raw.php?i=BKv0fMc3 2>/dev/null | jsonflatten | grep last | grep name | cut -f2 -d':' | strupper
```

  where http://pastebin.com/raw.php?i=BKv0fMc3 is a pastebin snippet containing

```
  {
    "name": {
      "last": "hirani",
      "middle": "prakash",
      "first": "saurabh"
    },
    "rank": {
      "last": "3",
      "middle": "2",
      "first": "1"
    }
  }
```

### What this module isn't

* Replacement for shell utilities - shell commands like tr, awk, cut, etc. are
  indespensible and pyfunc's aim is to augment them by:
  * enriching your shell with python's standard library functions.
  * reducing development time by enabling developers to write utilities in
    python and providing the interface to call them.

### Where do we go from here

* This module is relatively new and is work in progress. Design and feature
  level feedback is welcome.

### TODO

- Add basic tests. (I know - should've added them from the start.)
- Review more use cases and see if the current design survives their test.
- Use docopt instead of argparse (easier to make man pages with docopt).

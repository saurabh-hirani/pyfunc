pyfunc
======

Call python functions from your shell

Why - http://saurabh-hirani.github.io/writing/2015/08/14/pyfunc/

### Install 

pip install pyfunc

### Examples

* For builtin functions - just call them without any module prefix. For others,
  prefix them by their module name.

```
  $ pyfunc -m range -a 1 7 2
  1
  3
  5

  $ pyfunc -m string.upper -a test
  TEST

  $ pyfunc -m string.replace -a 'analyze what' 'what' 'this'
  analyze this
```

* Arguments can also be read from standard input by providing '-' symbol

```
  $ echo 1 | pyfunc -m range -a - 7 2
  1
  3
  5
```

* If the function takes only one argument (or others are optional),
  there is no need to give -a if you are feeding it from stdin

```
  $ echo TeSt | pyfunc -m string.swapcase
  tEsT
```

* Method signatures are assumed - if what you pass looks like an int - we wil
  convert it to int before passing it to the target function. However, if the
  user wants to explicitly specify method signature - he can do so. Apart from
  str/int - there is basic support to pass in other data types (list for now)

```
  $ pyfunc -m string.join -s list,str -a "Good news everyone" " burp! "
  Good burp! news burp! everyone

  $ pyfunc -m sum -s list:int,str -a "1 2 3"
  6
```

* For return values - you can print output in 3 ways:
  - shell (default) - print strings as they are, list and dicts by iterating
    over them
  - raw\_json
  - pretty\_json

```
  $ curl http://headers.jsontest.com/ 2>/dev/null | pyfunc -m pyfunc.utils.json_read -a -
  Host: headers.jsontest.com
  Accept: */*
  User-Agent: curl/7.32.0

  $ curl http://headers.jsontest.com/ 2>/dev/null | pyfunc -m pyfunc.utils.json_read -p raw_json -a -
  {"Host": "headers.jsontest.com", "Accept": "*/*", "User-Agent": "curl/7.32.0"}

  $ curl http://headers.jsontest.com/ 2>/dev/null | pyfunc -m pyfunc.utils.json_read -p pretty_json -a -
  {
      "Host": "headers.jsontest.com", 
      "Accept": "*/*", 
      "User-Agent": "curl/7.32.0"
  }
```

* pyfunc provides some basic utility functions which are present in pyfunc.utils

```
  $ curl http://pastebin.com/raw.php?i=BKv0fMc3 2>/dev/null | pyfunc -m pyfunc.utils.json_flatten 
  rank.first: 1
  rank.middle: 2
  rank.last: 3
  name.first: dwight
  name.middle: kurt
  name.last: schrute
```

* The right use case would be to create aliases out of commonly used functions
  and use them in your command pipelines:

```
  $ alias jsonflatten='pyfunc -m pyfunc.utils.json_flatten -a'
  $ alias strupper='pyfunc -m string.upper -a'
  $ curl http://pastebin.com/raw.php?i=BKv0fMc3 2>/dev/null | jsonflatten | grep first | grep name | cut -f2 -d':' | strupper
  DWIGHT
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

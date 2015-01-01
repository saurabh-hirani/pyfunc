pyfunc
======

Call python functions from your shell

Install 
====

./install.sh

Uninstall 
====

./uninstall.sh

Examples
====

  echo test | pyfunc -m string.upper

  pyfunc -m string.upper -a test

  pyfunc -m pyfunc.shell\_utils.json\_flatten -a nested\_json\_file

TODO
====

- More documentation
- Pip it

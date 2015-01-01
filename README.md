pyfunc
======

Call python functions from your shell

### Install 

./install.sh

### Uninstall 

./uninstall.sh

### Examples

    echo test | pyfunc -m string.upper

    pyfunc -m range -a 1 5 2

    pyfunc -m string.upper -a test

    pyfunc -m pyfunc.shell_utils.json_flatten -a nested_json_file

### TODO

- Pip it
- Usage documentation
- Use docopt instead of argparse

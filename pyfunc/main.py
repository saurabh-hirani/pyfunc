#!/usr/bin/env python

import argparse
import fileinput
import importlib
import re
import sys
from collections import namedtuple
import __builtin__
import json

def _print_shell(output):
  """ Print output to be consumed by shell """
  output_type = str(type(output))
  if 'list' in output_type or 'set' in output_type:
    for val in output:
      print val
  elif 'dict' in output_type:
    for k, v in output.iteritems():
      print k + ': ' + str(v)
  else:
    print output

def _print_json(output, indent=False):
  """ Print output as json """
  if indent:
    print json.dumps(output, indent=4)
    return
  print json.dumps(output)

def print_output(output, print_as):
  """ Print output returned by method call """
  if print_as == 'shell':
    _print_shell(output)
  elif print_as == 'raw_json':
    _print_json(output)
  elif print_as == 'pretty_json':
    _print_json(output, indent=True)
  return

def call_method(meth, args):
  """ Call the method and return output """
  return meth(*args)

def update_args(parsed_args):
  """ Process and enrich the args """
  mod, meth = None, None

  # check if the method is prefixed by a module
  mod_meth = parsed_args.meth.rsplit('.', 1)
  if len(mod_meth) == 1:
    meth = mod_meth[0]
  else:
    mod, meth = mod_meth

  # get the target module and method
  if mod:
    mod = importlib.import_module(mod)
  else:
    mod = __builtin__

  meth = getattr(mod, meth)
  parsed_args.mod, parsed_args.meth = mod, meth

  # check if user passed any args
  if not parsed_args.args:
    if parsed_args.read_stdin:
      parsed_args.args.append('-')

  # replaced stdin symbol with stuff from stdin
  updated_args = []
  for arg in parsed_args.args:
    if arg == '-' and parsed_args.read_stdin:
      updated_args.append(''.join(fileinput.input(arg)).rstrip())
      continue
    updated_args.append(arg)

  parsed_args.args = updated_args

  # assume argtypes as per args - unless specified otherwise
  if not parsed_args.methsig:
    # derive the arg types
    for arg in parsed_args.args:
      if re.match('^\d+$', arg):
        parsed_args.methsig.append(int)
      elif re.match('^\d+\.\d+$', arg):
        parsed_args.methsig.append(float)
      else:
        parsed_args.methsig.append(str)
  else:
    # arg types specified in meth sig - use them
    methsig_strs = parsed_args.methsig.split(',')
    actual_methsig = []
    for type_str in methsig_strs:
      found_type = None
      # skip the arg type of list - as it requires further processing
      if type_str.startswith('list'):
        found_type = type_str
      else:
        found_type = getattr(__builtin__, argtype_str.strip())
      actual_methsig.append(found_type)
      parsed_args.methsig = actual_methsig

  # if there are no args to process - return
  if not parsed_args.args:
    return parsed_args

  # found the arg types - convert each arg into its specified argtype
  converted_args = []
  for arg, argtype in zip(parsed_args.args, parsed_args.methsig):
    # handle case for list separately
    if str(argtype).startswith('list'):
      # if user intends the value of arg to be taken from stdin
      if arg == '-':
        arg = ''.join(fileinput.input(argval)).rstrip()

      # assume that each element of list is of type string, unless specified
      # otherwise
      each_argtype = str
      if ':' in argtype:
        each_argtype = getattr(__builtin__, argtype.split(':')[1].strip())
      converted_args.append([each_argtype(x) for x in arg.split()])
    else:
      converted_args.append(argtype(arg))

  parsed_args.args = converted_args
  return parsed_args

def parse_cmdline(args):
  """ Parse user input """
  desc = 'Call python methods from the cmdline'
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('-m', '--meth', help='method to call', required=True)
  parser.add_argument('-s', '--methsig',
                      help='method signature comma sep - builtin|list:builtin',
                      default=[])
  parser.add_argument('-a', '--args', help='method args',
                      nargs=argparse.REMAINDER, default=[])
  parser.add_argument('--read_stdin', help='takes args from stdin?',
                      action='store_true', dest='read_stdin')
  parser.add_argument('-p', '--print_as', help='Explicity print returned output',
                      default='shell')
  parser.set_defaults(read_stdin=True)
  parsed_args = parser.parse_args()
  return parsed_args

def main():
  """ Parse input, call method, return output """
  args = sys.argv[1:]
  parsed_args = parse_cmdline(args)
  callerinfo = update_args(parsed_args)
  output = call_method(callerinfo.meth, callerinfo.args)
  if parsed_args.print_as != 'none':
    print_output(output, parsed_args.print_as)
  return 0

if __name__ == '__main__':
  sys.exit(main())

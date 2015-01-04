#!/usr/bin/env python

import argparse
import fileinput
import importlib
import re
import sys
from collections import namedtuple
import __builtin__
import json

class PyfuncPrinter(object):
  """ Print output as required by print_as option """

  def _print_shell(self):
    """ Print output to be consumed by shell """
    printable = []
    data_type = str(type(self.data))
    if 'list' in data_type or 'set' in data_type:
      for val in self.data:
        printable.append(str(val))
    elif 'dict' in data_type:
      for k, v in self.data.iteritems():
        printable.append(k + ': ' + str(v))
    else:
        printable.append(str(data))
    return printable

  def _print_raw_json(self):
    """ Print output as raw json """
    return [json.dumps(self.data)]

  def _print_pretty_json(self):
    """ Print output as pretty json """
    return [json.dumps(self.data, indent=4)]

  printers = {
    'shell'   :    _print_shell,
    'raw_json':    _print_raw_json,
    'pretty_json': _print_pretty_json,
  }

  def __init__(self, data, print_as='shell', line_sep='\n'):
    # validate the input
    if print_as not in self.printers:
      raise ValueError('Invalid value provided for print_as - %s' % print_as)
    self.data = data
    self.print_as = print_as
    self.line_sep = line_sep
    # create a printable string of the data as per the type
    self.printable = self.line_sep.join(self.printers[print_as](self))

  def __str__(self):
    """ Return a printable string of print_as type """
    return self.printable

def call_method(meth, args):
  """ Call the method and return output """
  return meth(*args)

def _get_call_info(user_args):
  """ Process and enrich the args """
  mod, meth = None, None

  # check if the method is prefixed by a module
  mod_meth = user_args.meth.rsplit('.', 1)
  if len(mod_meth) == 1:
    meth = mod_meth[0]
  else:
    mod, meth = mod_meth

  # get the target module and method
  mod = importlib.import_module(mod) if mod else __builtin__

  meth = getattr(mod, meth)
  user_args.mod, user_args.meth = mod, meth

  # check if user passed any args
  if not user_args.args:
    if user_args.read_stdin:
      user_args.args.append('-')

  # replaced stdin symbol with stuff from stdin
  updated_args = []
  for arg in user_args.args:
    if arg == '-' and user_args.read_stdin:
      updated_args.append(''.join(fileinput.input(arg)).rstrip())
      continue
    updated_args.append(arg)

  user_args.args = updated_args

  # assume argtypes as per args - unless specified otherwise
  if not user_args.methsig:
    # derive the arg types
    for arg in user_args.args:
      if re.match('^\d+$', arg):
        user_args.methsig.append(int)
      elif re.match('^\d+\.\d+$', arg):
        user_args.methsig.append(float)
      else:
        user_args.methsig.append(str)
  else:
    # arg types specified in meth sig - use them
    methsig_strs = user_args.methsig.split(',')
    actual_methsig = []
    for type_str in methsig_strs:
      found_type = None
      # skip the arg type of list - as it requires further processing
      found_type = type_str if type_str.startswith('list') else getattr(__builtin__, type_str.strip())
      actual_methsig.append(found_type)
      user_args.methsig = actual_methsig

  # if there are no args to process - return
  if not user_args.args:
    return user_args

  # found the arg types - convert each arg into its specified argtype
  converted_args = []
  for arg, argtype in zip(user_args.args, user_args.methsig):
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

  user_args.args = converted_args
  return user_args

def _parse_cmdline(args):
  """ Parse user input """
  desc = 'Call python methods from the cmdline'
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('-m', '--meth',
                      help='fqdn of method to call e.g. string.upper,range',
                      required=True)
  parser.add_argument('-s', '--methsig',
                      help='method signature comma sep e.g. int,list,list:int',
                      default=[])
  parser.add_argument('-a', '--args', help='method args',
                      nargs=argparse.REMAINDER, default=[])
  parser.add_argument('-r', '--read_stdin', help='takes args from stdin?',
                      action='store_true', dest='read_stdin')
  parser.add_argument('-p', '--print_as', help='print_as shell,raw_json,pretty_json',
                      default='shell')
  parser.set_defaults(read_stdin=True)
  user_args = parser.parse_args(args=args)
  return user_args

def get_call_info(args):
  user_args = _parse_cmdline(args)
  call_info = _get_call_info(user_args)
  return call_info

def main():
  """ Parse input, call method, return output """
  call_info = get_call_info(sys.argv[1:])
  print call_info
  output = call_method(call_info.meth, call_info.args)
  if call_info.print_as != 'none':
    print PyfuncPrinter(output, call_info.print_as)
  return 0

if __name__ == '__main__':
  sys.exit(main())

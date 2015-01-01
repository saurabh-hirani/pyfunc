import os
import json
import fileinput

def flatten_ds(data_struct, key="", path="", flattened=None):
  """ Flatten a nested data structure """
  if flattened is None:
    flattened = {}
  if type(data_struct) not in(dict, list):
    flattened[((path + ".") if path else "") + key] = data_struct
  elif isinstance(data_struct, list):
    for i, item in enumerate(data_struct):
      flatten_ds(item, "%d" % i, (path + '.' + key if path else key),
                 flattened)
  else:
    for new_key, value in data_struct.items():
      flatten_ds(value, new_key, (path + '.' + key if path else key),
                 flattened)
  return flattened

def f_is_subset(f1, f2):
  """ Check if f1 is subset of f2 """
  f1_data = set(open(f1).readlines())
  f2_data = set(open(f2).readlines())
  return f1_data.issubset(f2_data)

def f_set_diff(f1, f2):
  """ Find set difference between 2 files """
  # put rstrip as an improvement
  f1_data = set([x.rstrip() for x in open(f1).readlines()])
  f2_data = set([x.rstrip() for x in open(f2).readlines()])
  return f1_data - f2_data

def json_read(json_file, compound_key=None):
  """ Read a json file """
  if os.path.exists(json_file):
    json_str = ''.join(fileinput.input(json_file))
  else:
    json_str = json_file
  ds = json.loads(json_str)

  if compound_key is not None:
    if compound_key == 'keys':
      ds = ds.keys()
    elif compound_key == 'nkeys':
      ds = len(ds.keys())
    elif compound_key == 'values':
      ds = ds.values()
    else:
      for key in compound_key.split(':'):
        ds = ds[key]

  return ds

def json_flatten(json_file):
  """ Flatten json data structure """
  return flatten_ds(json_read(json_file))

def str_slice(str1, start=None, stop=None, step=None):
  """ Perform a string slice """
  if step is None:
    step = 1
  return str1[start:stop:step]

def str_reverse(str1):
  return str_slice(str1, step=-1)

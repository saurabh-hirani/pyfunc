import pyfunc.main
import __builtin__

default_test_args = ['-m', 'range', '-a', '1', '10']

def test_args():
  call_info = pyfunc.main.get_call_info(default_test_args)
  assert(range, call_info.meth)
  assert([int, int], call_info.methsig)
  assert(__builtin__, call_info.mod)
  assert([1, 10], call_info.args)

def test_default_args():
  call_info = pyfunc.main.get_call_info(default_test_args)
  assert('shell', call_info.print_as)
  assert(True, call_info.read_stdin)

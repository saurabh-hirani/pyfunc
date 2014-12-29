from distutils.core import setup
setup(name='pyfunc',
      license='GPL v2',
      version='1.0',
      description='Call python functions from your shell',
      author='Saurabh Hirani',
      author_email='saurabh.hirani@gmail.com',
      scripts=['callfunc.py'],
      py_modules=['shell_utils'])

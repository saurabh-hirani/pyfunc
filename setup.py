from setuptools import setup, find_packages
setup(
  name='pyfunc',
  license='GPL v2',
  version='0.1',
  url='https://github.com/saurabh-hirani/pyfunc',
  description=('Call python functions from your shell'),
  author='Saurabh Hirani',
  author_email='saurabh.hirani@gmail.com',
  packages=find_packages(),
  entry_points = {
    'console_scripts': [
      'pyfunc = pyfunc.main:main',
    ]
  }
)

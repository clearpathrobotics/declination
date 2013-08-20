## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

args = generate_distutils_setup(
    packages=['geomag', 'declination'],
    package_dir={'': 'src'})

setup(**args)

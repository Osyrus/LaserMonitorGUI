import py2exe
from distutils.core import setup
import sys

sys.argv.append('py2exe')

setup(
	options = {'py2exe': {'bundle_files': 2, 'compressed': True,"includes":["Panels", "Menus"]}},
	windows = [{"script": "Main.py"}],
	zipfile = None,
)
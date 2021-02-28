"""
Robot Framework from sublime is a autocompletion plugin for Sublime Text 3
"""
import sys
# import os
# from string import Template
from .commands import *

if sys.version_info < (3, 3):
    raise RuntimeError('Plugin only works with Sublime Text 3')


def plugin_loaded():
    print('Robot beautify plugin loaded...')

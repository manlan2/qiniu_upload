#-*- coding: utf-8 -*-
import platform
from termcolor import colored

__version__ = '0.1.3'

def print_color(message, color):
    if platform.system().lower() == 'windows':
        print(message)
    else:
        print(colored(message, color))

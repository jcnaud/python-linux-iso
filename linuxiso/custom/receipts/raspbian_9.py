# coding: utf-8
import os
import time
# from jinja2 import Environment,FileSystemLoader
from jinja2 import Template
import tempfile

# Local import
from linuxiso.ressources.tools import run_cmd




def customRaspbian9(self, file_iso):
    """
    Transform imf Raspbian 9
    params file_iso : img of Raspbian
    """
    dir_build = self.conf['dir_build']['path']
    dir_input = self.conf['dir_input']['path']
    iso_ouput = self.conf['iso_ouput']['path']
    dir_loopdir = dir_build + os.sep + 'loopdir'  # Directory to mount the iso
    dir_cd = dir_build + os.sep + 'cd'            # Directory to copy and modify the iso
    dir_irmod = dir_build + os.sep + 'irmod'      # Directory to copy and modify the init.rd
    iso_input = dir_input+os.sep+self.conf['custom'][file_iso]['iso_input']
    file_template = os.path.dirname(os.path.realpath(__file__))+os.sep+'templates'+os.sep+self.conf['custom'][file_iso]['template']

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from os import listdir
from os.path import isdir, isfile, join
import sys
import getopt
import re
import string
import time
#from jinja2 import Environment,FileSystemLoader
from jinja2 import Template, FileSystemLoader, Environment

import subprocess          # Used to run bash command
from shlex import split    # Used to split bash command automaticaly

import logging         # for logging mode/level
import argparse        # for command line usage (with options/arguments)

import tempfile


# Local Import
from linuxiso.ressources.tools import run_cmd
from linuxiso.custom.receipts.debian_9 import (custom_debian_9,
    custom_debian_9_soft)


class Custom(object):
    """Custom iso"""

    def __init__(self, conf=None):
        self.conf = conf

    def getIsoStatus(self):
        """
        Check custom iso/image status
        return : dict with status
        """
        iso_status = {}
        l_iso = self.conf['custom']
        dir_isocustom = self.conf['dir_isocustom']['path']

        for i in l_iso.keys():
            if os.path.isfile(dir_isocustom+os.sep+i):
                iso_status[i] = {"file" : "Exist" }
            else:
                iso_status[i] = {"file" : "Not exist" }

        return iso_status

    def create(self, file_iso, context):
        """
        Create custom iso/image from a other normal iso
        params file_iso : Name iso used
        """
        #print(json.dumps(self.conf, sort_keys=True, indent=4))
        #subprocess.run(["ls", "-l", "/dev/null"], stdout=subprocess.PIPE)

        # Deduce iso_input
        dir_input = self.conf['dir_input']['path']
        iso_input = dir_input+os.sep+self.conf['custom'][file_iso]['iso_base']

        # Deduce iso output
        iso_ouput = os.path.join(self.conf['dir_isocustom']['path'], file_iso)

        # Create build directory
        dir_build = self.conf['dir_build']['path']
        if not os.path.isdir(dir_build):
            os.makedirs(dir_build)
        dir_build_tmp = tempfile.mkdtemp(dir=dir_build)


        (iso_input, iso_ouput, dir_build_tmp, context)

        # Clean Build directory "Dangerous"
        #if not os.path.isdir(dir_build):
        #  os.rmdir(dir_build)
        try:
            if self.conf['custom'][file_iso]['transfom'] == 'customDebian9':
                custom_debian_9(iso_input, iso_ouput, dir_build_tmp, context)
            elif self.conf['custom'][file_iso]['transfom'] == 'customDebian9soft':
                custom_debian_9_soft(iso_input, iso_ouput, dir_build_tmp, context)
            elif self.conf['custom'][file_iso]['transfom'] == 'customUbuntu16soft':
                custom_ubuntu_16_soft(iso_input, iso_ouput, dir_build_tmp, context)
            elif self.conf['custom'][file_iso]['transfom'] == 'customUbuntu17soft':
                custom_ubuntu_17_soft(iso_input, iso_ouput, dir_build_tmp, context)
            else:
                assert True, "Transformation not know"
        except Exception as e:
            raise Exception(e)
        finally:
            # == Big clean ==
            if os.path.isdir(dir_build):
                #print('rm -r '+dir_build)
                run_cmd('rm -r '+dir_build)

    def delete(self, file_iso):
        """
        Delete custom iso/image from a other normal iso
        params file_iso : Name iso used
        """
        dir_isocustom = self.conf['dir_isocustom']['path']
        path_file = dir_isocustom+os.sep+file_iso

        if os.path.isfile(path_file):
            logging.info("Delete: "+path_file)
            os.remove(path_file)
        else:
            logging.warning("Iso "+path_file+" not exist. Nothing to delete")


    @staticmethod
    def render(path_template_file, context):
        """
        Simple function to use jinja2 template with file
        """
        path, filename = os.path.split(path_template_file)
        return Environment(
            loader=FileSystemLoader(path or './')
        ).get_template(filename).render(context)

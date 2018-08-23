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
from linuxiso.custom.receipts.debian_9 import (
    custom_debian_9,
    custom_debian_9_soft)


class Custom(object):
    """Custom iso"""

    def __init__(self, conf=None):
        self.conf = conf

    def list(self):
        """Get list of cusotm iso."""
        return sorted(list(self.conf['custom'].keys()))

    def status(self, iso):
        """
        Check custom iso/image status
        return : dict with status
        """
        dir_isocustom = self.conf['dir_isocustom']['path']

        if os.path.isfile(dir_isocustom+os.sep+iso):
            return {'is_exist': True}
        else:
            return {'is_exist': False}

    def status_all(self):
        """
        Check custom iso/image status
        return : dict with status
        """
        result = {}
        for iso in self.conf['custom'].keys():
            result[iso] = self.status(iso)
        return result

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


        # (iso_input, iso_ouput, dir_build_tmp, context)

        # Clean Build directory "Dangerous"
        #if not os.path.isdir(dir_build):
        #  os.rmdir(dir_build)
        try:
            if self.conf['custom'][file_iso]['transfom'] == 'customDebian9':
                custom_debian_9(iso_input, iso_ouput, dir_build_tmp, context)
            elif self.conf['custom'][file_iso]['transfom'] == 'customDebian9soft':
                custom_debian_9_soft(iso_input, iso_ouput, dir_build_tmp, context)
            # elif self.conf['custom'][file_iso]['transfom'] == 'customUbuntu16soft':
            #     custom_ubuntu_16_soft(iso_input, iso_ouput, dir_build_tmp, context)
            # elif self.conf['custom'][file_iso]['transfom'] == 'customUbuntu17soft':
            #     custom_ubuntu_17_soft(iso_input, iso_ouput, dir_build_tmp, context)
            else:
                assert True, "Transformation not know"
        except Exception as e:
            raise Exception(e)
        finally:
            # Clean build directory
            if os.path.isdir(dir_build):
                run_cmd('rm -r '+dir_build)

    def remove(self, iso):
        """
        Delete custom iso/image from a other normal iso
        params file_iso : Name iso used

        >>> custom.remove("Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso")
        """
        file_iso = self.conf['dir_isocustom']['path']+os.sep+iso

        if os.path.isfile(file_iso):
            os.remove(file_iso)

    def remove_all(self):
        """ Remove all iso

        >>> download.remove_all()
        """
        for iso in self.conf['download'].keys():
            self.remove(iso)


    @staticmethod
    def render(path_template_file, context):
        """
        Simple function to use jinja2 template with file
        """
        path, filename = os.path.split(path_template_file)
        return Environment(
            loader=FileSystemLoader(path or './')
        ).get_template(filename).render(context)

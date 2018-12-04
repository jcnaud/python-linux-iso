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
import yaml


# Local Import
from linuxiso.ressources.tools import run_cmd
from linuxiso.custom.receipts.debian_9 import (
    custom_debian_9,
    custom_debian_9_soft)


class Custom(object):
    """Custom iso"""

    def __init__(self, conf=None):
        self.conf = conf
        dir_path = os.path.dirname(os.path.realpath(__file__))
        conf_receipts = os.path.join(dir_path, 'receipts.yaml')
        with open(conf_receipts, "r") as f:
            self.receipts = yaml.safe_load(f)

    def list(self):
        """Get list of cusotm iso."""
        return sorted(list(self.conf['custom']['iso'].keys()))

    def status(self, iso):
        """
        Check custom iso/image status
        return : dict with status
        """
        dir_isocustom = self.conf['general']['dir_isocustom']

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

    def create(self, file_iso):
        """
        Create custom iso/image from a other normal iso
        params file_iso : Name iso used
        """
        #print(json.dumps(self.conf, sort_keys=True, indent=4))
        #subprocess.run(["ls", "-l", "/dev/null"], stdout=subprocess.PIPE)

        # Deduce iso_input

        dir_input = self.conf['general']['dir_input']
        sub_conf = self.conf['custom']['iso'][file_iso]
        receipt = self.receipts[sub_conf['receipt']]

        iso_input = dir_input+os.sep+receipt['iso_base']
        template_vars = sub_conf['vars']
        # Deduce iso output
        iso_ouput = os.path.join(self.conf['general']['dir_isocustom'], file_iso)

        # Create build directory
        dir_build = self.conf['general']['dir_build']
        if not os.path.isdir(dir_build):
            os.makedirs(dir_build)
        dir_build_tmp = tempfile.mkdtemp(dir=dir_build)


        # (iso_input, iso_ouput, dir_build_tmp, context)

        # Clean Build directory "Dangerous"
        #if not os.path.isdir(dir_build):
        #  os.rmdir(dir_build)
        try:
            if receipt['transfom'] == 'customDebian9':
                custom_debian_9(iso_input, iso_ouput, dir_build_tmp, template_vars)
            elif receipt['transfom'] == 'customDebian9soft':
                custom_debian_9_soft(iso_input, iso_ouput, dir_build_tmp, template_vars)
            # elif self.conf['custom'][file_iso]['transfom'] == 'customUbuntu16soft':
            #     custom_ubuntu_16_soft(iso_input, iso_ouput, dir_build_tmp, context)
            # elif self.conf['custom'][file_iso]['transfom'] == 'customUbuntu17soft':
            #     custom_ubuntu_17_soft(iso_input, iso_ouput, dir_build_tmp, context)
            else:
                assert True, "Transformation unknow"
        except Exception as e:
            raise Exception(e)
        finally:
            # Clean build directory
            if os.path.isdir(dir_build):
                run_cmd('rm -r '+dir_build)
            #pass

    def remove(self, iso):
        """
        Delete custom iso/image from a other normal iso
        params file_iso : Name iso used

        >>> custom.remove("Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso")
        """
        file_iso = self.conf['general']['dir_isocustom']+os.sep+iso

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

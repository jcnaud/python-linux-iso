#!/usr/bin/env python
# coding: utf-8

import os
from os import listdir
from os.path import  isdir, isfile, join
import sys, getopt
import re
import string

import urllib.request

from urllib.parse import urlparse
import http.client

import json
import yaml
from jsonschema import validate

import logging         # for logging mode/level
import argparse        # for command line usage (with options/arguments)

## Local Import
import tools


class Download(object):
    """
    Class manage download and verify iso
    """
    def __init__(self,conf_file="settings.yaml", conf=None):
        """Init"""
        self.conf = self._load_conf(conf_file, conf)

    def _load_conf(self, conf_file, conf=None):
        """
        Load & check configuration
        """
        if conf:
            conf_not_valided = conf # Load conf from "dict"
        else:
            with open(conf_file, "r") as f:
                conf_not_valided = yaml.load(f) # Load conf from "file"
        
        with open("linuxiso_jsonschema.json", "r") as f:
            dict_schema = json.load(f)

        validate(conf_not_valided, dict_schema) # If no exception, the conf is valided
        return conf_not_valided

    def getIsoStatus(self):
        """
        CheckIso status
        return : dict with status
        """
        iso_status = {}
        l_iso = self.conf['download']
        dir_save = self.conf['dir_save']['path']

        for i in l_iso.keys():
            url = l_iso[i]["url_iso"]
            if os.path.isfile(dir_save+os.sep+i):
                iso_status[i] = {"file" : "Exist" }
            else:
                iso_status[i] = {"file" : "Not exist" }

            if self._checkUrl(url):
                iso_status[i]["url"] = "Exist"
            else :
                iso_status[i]["url"] = "Not exist"

        return iso_status

    def displayIsoStatus(self):
        pass

    def _checkUrl(self, url):
        """ Check if url exist
        return bool : """
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'

        try:
            urllib.request.urlopen(request)
            return True
        except :
            return False
    
    def download(self, id_iso):
        """Download one iso"""
        url_iso = self.conf['download'][id_iso]['url_iso']
        dir_save = self.conf['dir_save']['path']
        file_iso = dir_save+os.sep+id_iso

        if not os.path.isdir(dir_save):
            os.makedirs(dir_save)
        
        if not os.path.exists(file_iso):
            logging.info("Download : "+file_iso)
            urllib.request.urlretrieve(url_iso, file_iso)
        else:
            logging.info("File exist, do nothing because already downloaded")


    def downloadall(self):
        """ Download all iso"""
        for i in self.conf['download'].keys():
            self.download(i)

    def remove(self, id_iso):
        """ Remove one iso"""
        pass
    
    def remove_all(self):
        """ Remove all iso"""
        pass

def main(args):
    """Parsing comnand line options/arguments"""

    if args: 

        # Manage "verbose" and "quiet" options
        if args.verbose == 0:       
            logging.basicConfig(level=logging.WARNING)
        elif args.verbose == 1:
            logging.basicConfig(level=logging.INFO)
        elif args.verbose >= 2:
            logging.basicConfig(level=logging.DEBUG)
        elif args.quiet:
            logging.basicConfig(level=logging.NOTSET)

        # Manage "config-file" options
        if args.config_file:
            di = Download(conf_file=args.config_file)
        else:
            di = Download()

        # Manage "list", "download", "download-all", "remove" and "remove-all" options
        if args.list:               # List iso/image status
            result = di.getIsoStatus()
            print(json.dumps(result, indent=4))
        elif args.download:         # Download one iso/image
            di.download(args.download)
        elif args.download_all:     # Download all iso/image
            di.downloadall()
        elif args.remove:           # Remove one iso/image
            di.remove(args.remove)
        elif args.remove_all():     # Remove all iso/image
            di.remove_all()
        

if __name__ == "__main__":
    """Entry point for command ligne usage (with options/arguments)"""

    parser = argparse.ArgumentParser(description='Program manage download of iso/image')

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list", 
        help="list iso status", 
        action="store_true")
    group.add_argument("-d", "--download", 
        help="download the iso/image",
        metavar="ISO_NAME")
    group.add_argument("-r", "--remove", 
        help="remove the iso/image",
        metavar="ISO_NAME")
    group.add_argument("-a", "--download-all", 
        help="download all iso/image",
        action="store_true")
    group.add_argument("-p", "--remove-all", 
        help="remove all iso/image", 
        action="store_true")

    parser.add_argument("-f", "--config-file", 
        help="load personnal configuration file (defaut: settings.yaml)",
        metavar="CONF_FILE")

    group_vq = parser.add_mutually_exclusive_group()
    group_vq.add_argument("-v", "-vv", "--verbose", 
        help="enable verbosity: -v = INFO, -vv = DEBUG ", 
        action="count",
        default=0)
    group_vq.add_argument("-q", "--quiet", 
        help="quiet mode", 
        action="store_true")
    

    ## TODO , if no option specified, print help
    args = parser.parse_args()
    main(args)
    

    # Exemple of comand ligne call:
    #   python download.py -d debian-9.2.1-strech-amd64-netinst.iso

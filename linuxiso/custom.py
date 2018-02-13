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
from jinja2 import Template

import subprocess          # Used to run bash command
from shlex import split    # Used to split bash command automaticaly

import json
import yaml
from   jsonschema import validate

import logging         # for logging mode/level
import argparse        # for command line usage (with options/arguments)

import tempfile

class Custom(object):
    """Custom iso"""

    def __init__(self, conf_file="settings.yaml", conf=None):
        self.conf = self._load_conf(conf_file)

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

    def create(self, file_iso):
        """
        Create custom iso/image from a other normal iso
        params file_iso : Name iso used
        """
        #print(json.dumps(self.conf, sort_keys=True, indent=4))
        #subprocess.run(["ls", "-l", "/dev/null"], stdout=subprocess.PIPE)

        if self.conf['custom'][file_iso]['transfom'] == 'customDebian9':
            self.custom_debian_9(file_iso)
        if self.conf['custom'][file_iso]['transfom'] == 'customDebian9soft':
            self.custom_debian_9_soft(file_iso)

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

    def custom_debian_9(self, file_iso):
        """
        Transform iso Debian 9
        params file_iso : Name of Debian 9 iso used
        """
        dir_build = self.conf['dir_build']['path']
        # Create build directory
        if not os.path.isdir(dir_build):
            os.makedirs(dir_build)
        dir_build_tmp = tempfile.mkdtemp(dir=dir_build)

        dir_save = self.conf['dir_save']['path']
        dir_isocustom = self.conf['dir_isocustom']['path']
        dir_loopdir = dir_build_tmp + os.sep + 'loopdir'  # Directory to mount the iso
        dir_cd = dir_build_tmp + os.sep + 'cd'            # Directory to copy and modify the iso
        dir_irmod = dir_build_tmp + os.sep + 'irmod'      # Directory to copy and modify the init.rd
        iso_base = dir_save+os.sep+self.conf['custom'][file_iso]['iso_base']
        file_template = os.path.dirname(os.path.realpath(__file__))+os.sep+'templates'+os.sep+self.conf['custom'][file_iso]['template']
        
        # Clean Build directory "Dangerous"
        #if not os.path.isdir(dir_build):
        #  os.rmdir(dir_build)

        try:
            # == Mount iso on loopdir
            os.makedirs(dir_loopdir)
            os.chdir(dir_loopdir) # Important

            self.run_cmd('fuseiso '+iso_base+' '+dir_loopdir)
            #self.run_cmd('mount -o loop '+iso_base+' '+dir_loopdir)
            
            time.sleep(1) # Important to avoid some mount latence bug

            # == Copy iso to cd
            os.makedirs(dir_cd)
            os.chdir(dir_cd)
            #self.run_cmd('7z x '+iso_base)
            self.run_cmd('rsync -a -H --exclude=TRANS.TBL '+dir_loopdir+os.sep+' '+dir_cd)
            
            # == Umount iso
            self.run_cmd('fusermount -u '+dir_loopdir)
            #self.run_cmd('umount '+dir_loopdir)

            # == Umount iso loopdir
            #self.run_cmd('umount '+dir_loopdir)
            #os.rmdir(dir_loopdir)
            
            # == extrate Init rd
            os.makedirs(dir_irmod)
            os.chdir(dir_irmod)
            self.run_cmd('gzip -d < '+dir_cd+'/install.amd/initrd.gz |\
                fakeroot -s ../initrd.fakeroot cpio  --extract --verbose --make-directories --no-absolute-filenames')


            # == Tempale preseed
            with open(file_template) as file:  
                data = file.read()
            template = Template(data)

            context = {
                'ansible_user_name' : 'ansible',
                'ansible_authorized_keys' : [
                    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxxDwYctg2ngBkR5Xuzz3NxGIxqY88nOVP1SOnAz24B3LfCn7EzpEHvUC/Dw+fGk0CmFEQZMBFc7vjOTVT1kk2wajX241y+zHd92JA1NFdxa8T2kg5xlkXK5zAvs5a/PRmTcijnSK1ynw1t+uglLgpj3UkhZ3OScfc8xmb1SPy/8carF44HavNI0/KTXjyuBuM3b+9GXChwMLI2ZNQZ+RAEVH5nsaLwPqWVHCe6JID2ApIHNq4kC/V9pRGsH1w4tApVspCJ4lnSlMxVLbnS+zdJpV2/UpaFv64VG5KTbkeNYBwg7EE6KVI+bU93AMZYI75UeEPafWT/WESDW9K1RbH root@edugastp'
                ]
            }

            data_preseed = template.render(context)
            
            os.chdir(dir_irmod)
            with open('./preseed.cfg','w') as file:  
                file.write(data_preseed)
            

            # == Compress and change init rd

            self.run_cmd('chmod u+w '+dir_cd+'/install.amd/initrd.gz')
            self.run_cmd(' find . | fakeroot -i ../initrd.fakeroot cpio -H newc --create --verbose | \
            gzip -9 > '+dir_cd+'/install.amd/initrd.gz')
            self.run_cmd('chmod u-w '+dir_cd+'/install.amd/initrd.gz')

            # == Menu start modification
            os.chdir(dir_cd)
            self.run_cmd("chmod u+w isolinux")
            self.run_cmd("sed -i 's/^default.*$/default auto/m' isolinux/isolinux.cfg")
            self.run_cmd("sed -i 's/^prompt.*$/prompt 1/m' isolinux/isolinux.cfg")
            self.run_cmd("sed -i 's/^timeout.*$/timeout 100/m' isolinux/isolinux.cfg")
            self.run_cmd("chmod u-w isolinux")

            # == Rebuild md5
            os.chdir(dir_cd)
            self.run_cmd('chmod u+w ./')
            self.run_cmd('chmod u+w md5sum.txt')
            self.run_cmd('rm md5sum.txt')
            self.run_cmd('md5sum `find -follow -type f` > md5sum.txt')
            self.run_cmd('chmod 444 md5sum.txt')
            self.run_cmd('chmod u-w ./')

            # == Create image
            os.chdir(dir_build_tmp)
            self.run_cmd('chmod u+w cd/isolinux/isolinux.bin')
            self.run_cmd('fakeroot genisoimage -o '+dir_isocustom+os.sep+file_iso+' -r -J -no-emul-boot -boot-load-size 4 \
                -boot-info-table -b isolinux/isolinux.bin -c isolinux/boot.cat ./cd')
            #-boot-info-table

            #self.run_cmd('chmod -R u+w '+dir_cd)
            #os.rmdir(dir_build)
        finally:
            # == Big clean ==
            if os.path.isdir(dir_cd):
                self.run_cmd('chmod -R u+rw '+dir_cd)
                #self.run_cmd('rm -r '+dir_cd)
            if os.path.isdir(dir_loopdir):
                if os.path.ismount(dir_loopdir):
                    self.run_cmd('fusermount -u '+dir_loopdir)
                #self.run_cmd('rm -r '+dir_loopdir)
            
        
        


    def custom_debian_9_soft(self, file_iso):
        """
        Transform iso Debian 9
        params file_iso : Name of Debian 9 iso used
        """
        dir_build = self.conf['dir_build']['path']
        # Create build directory
        if not os.path.isdir(dir_build):
            os.makedirs(dir_build)
        dir_build_tmp = tempfile.mkdtemp(dir=dir_build)
        dir_save = self.conf['dir_save']['path']
        dir_isocustom = self.conf['dir_isocustom']['path']
        dir_loopdir = dir_build_tmp + os.sep + 'loopdir'  # Directory to mount the iso
        dir_cd = dir_build_tmp + os.sep + 'cd'            # Directory to copy and modify the iso
        dir_irmod = dir_build_tmp + os.sep + 'irmod'      # Directory to copy and modify the init.rd
        iso_base = dir_save+os.sep+self.conf['custom'][file_iso]['iso_base']
        file_template = os.path.dirname(os.path.realpath(__file__))+os.sep+'templates'+os.sep+self.conf['custom'][file_iso]['template']
        
        # Clean Build directory "Dangerous"
        #if not os.path.isdir(dir_build):
        #  os.rmdir(dir_build)


        try:
            # == Mount iso on loopdir
            os.makedirs(dir_loopdir)
            os.chdir(dir_loopdir) # Important

            self.run_cmd('fuseiso '+iso_base+' '+dir_loopdir)
            #self.run_cmd('mount -o loop '+iso_base+' '+dir_loopdir)
            
            time.sleep(1) # Important to avoid some mount latence bug

            # == Copy iso to cd
            os.makedirs(dir_cd)
            os.chdir(dir_cd)
            #self.run_cmd('7z x '+iso_base)
            self.run_cmd('rsync -a -H --exclude=TRANS.TBL '+dir_loopdir+os.sep+' '+dir_cd)
            
            # == Umount iso
            self.run_cmd('fusermount -u '+dir_loopdir)
            #self.run_cmd('umount '+dir_loopdir)

            # == Custom grub menu
            os.chdir(dir_cd)
            data_grub_menu = ("\n"
                "label netinstall \n"
                "    menu label ^Install auto via preseed \n"
                "    menu default \n"
                "    kernel /install.amd/vmlinuz \n"
                "    append auto=true vga=normal file=/cdrom/preseed.cfg initrd=/install.amd/initrd.gz locale=fr_FR.UTF-8 console-keymaps-at/keymap=fr-latin9\n"
                "")

            self.run_cmd('chmod u+w isolinux/txt.cfg')
            with open("isolinux/txt.cfg", "a") as f:
                f.write(data_grub_menu)
            self.run_cmd('chmod u-w isolinux/txt.cfg')

            # == Menu start modification
            os.chdir(dir_cd)
            self.run_cmd("chmod u+w isolinux")
            #self.run_cmd("sed -i 's/^default.*$/default auto/m' isolinux/isolinux.cfg")
            #self.run_cmd("sed -i 's/^prompt.*$/prompt 1/m' isolinux/isolinux.cfg")
            self.run_cmd("sed -i 's/^timeout.*$/timeout 100/m' isolinux/isolinux.cfg")
            self.run_cmd("chmod u-w isolinux")

            # == Tempale preseed
            with open(file_template) as file:  
                data = file.read()
            template = Template(data)

            context = {
                'ansible_user_name' : 'ansible',
                'ansible_authorized_keys' : [
                    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxxDwYctg2ngBkR5Xuzz3NxGIxqY88nOVP1SOnAz24B3LfCn7EzpEHvUC/Dw+fGk0CmFEQZMBFc7vjOTVT1kk2wajX241y+zHd92JA1NFdxa8T2kg5xlkXK5zAvs5a/PRmTcijnSK1ynw1t+uglLgpj3UkhZ3OScfc8xmb1SPy/8carF44HavNI0/KTXjyuBuM3b+9GXChwMLI2ZNQZ+RAEVH5nsaLwPqWVHCe6JID2ApIHNq4kC/V9pRGsH1w4tApVspCJ4lnSlMxVLbnS+zdJpV2/UpaFv64VG5KTbkeNYBwg7EE6KVI+bU93AMZYI75UeEPafWT/WESDW9K1RbH root@edugastp'
                ]
            }

            data_preseed = template.render(context)
            
            os.chdir(dir_cd)
            self.run_cmd('chmod u+w .')
            with open('./preseed.cfg','w') as file:  
                file.write(data_preseed)
            self.run_cmd('chmod u-w .')


            # == Rebuild md5
            os.chdir(dir_cd)
            self.run_cmd('chmod u+w ./')
            self.run_cmd('chmod u+w md5sum.txt')
            self.run_cmd('rm md5sum.txt')
            self.run_cmd('md5sum `find -follow -type f` > md5sum.txt')
            self.run_cmd('chmod 444 md5sum.txt')
            self.run_cmd('chmod u-w ./')

            # == Create image
            os.chdir(dir_build_tmp)
            self.run_cmd('chmod u+w cd/isolinux/isolinux.bin')
            self.run_cmd('fakeroot genisoimage -o '+dir_isocustom+os.sep+file_iso+' -r -J -no-emul-boot -boot-load-size 4 \
                -boot-info-table -b isolinux/isolinux.bin -c isolinux/boot.cat ./cd')
            #-boot-info-table


        finally:
            # == Big clean ==
            if os.path.isdir(dir_cd):
                self.run_cmd('chmod -R u+rw '+dir_cd)
                #self.run_cmd('rm -r '+dir_cd)
            if os.path.isdir(dir_loopdir):
                if os.path.ismount(dir_loopdir):
                    self.run_cmd('fusermount -u '+dir_loopdir)
                #self.run_cmd('rm -r '+dir_loopdir)
            print(dir_build_tmp)

    def customRaspbian9(self, file_iso):
        """
        Transform imf Raspbian 9
        params file_iso : img of Raspbian
        """
        dir_build = self.conf['dir_build']['path']
        dir_save = self.conf['dir_save']['path']
        dir_isocustom = self.conf['dir_isocustom']['path']
        dir_loopdir = dir_build + os.sep + 'loopdir'  # Directory to mount the iso
        dir_cd = dir_build + os.sep + 'cd'            # Directory to copy and modify the iso
        dir_irmod = dir_build + os.sep + 'irmod'      # Directory to copy and modify the init.rd
        iso_base = dir_save+os.sep+self.conf['custom'][file_iso]['iso_base']
        file_template = os.path.dirname(os.path.realpath(__file__))+os.sep+'templates'+os.sep+self.conf['custom'][file_iso]['template']


    @staticmethod
    def run_cmd(cmd):
        """
        Run a command
        if error, print and raise
        params cmd : String commande
        return out
        """
        logging.debug('Run command "'+cmd+'"')
        try:
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            process.check_returncode()
            
        except Exception as e:
            logging.exception(str(e) +"\nCMD_SHELL : "+cmd+"\nSTDOUT : "+process.stdout.decode()+"\nSTDERR : "+process.stderr.decode(), exc_info=True)
            #logging.critical("{CDM : "+cmd+", "} : "+cmd)
            #logging.critical("STDOUT : "+process.stdout.decode())
            #logging.critical("STDERR : "+process.stderr.decode())
            #raise e

        return process.stdout.decode()
        

    @staticmethod
    def render(path_template_file, context):
        """
        Simple function to use jinja2 template with file
        """
        path, filename = os.path.split(path_template_file)
        return Environment(
            loader=FileSystemLoader(path or './')
        ).get_template(filename).render(context)


def main(agrs):
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
            ci = Custom(conf_file=args.config_file)
        else:
            ci = Custom()

        # Manage "list", "create", "delete"
        if args.list:             # List custom iso/image status
            result = ci.getIsoStatus()
            print(json.dumps(result, indent=4))
        elif args.create:         # Create one custom iso/image
            ci.create(args.create)
        elif args.delete:         # Delete one custom iso/image
            ci.delete(args.delete)

if __name__ == "__main__":
    """Entry point for command ligne usage (with options/arguments)"""

    parser = argparse.ArgumentParser(description='Program custom iso/image')

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list", 
        help="list custom iso status", 
        action="store_true")
    group.add_argument("-c", "--create", 
        help="create custom iso/image",
        metavar="ISO_NAME")
    group.add_argument("-d", "--delete", 
        help="delete custom iso/image",
        metavar="ISO_NAME")

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
    #   python custom.py -c Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso


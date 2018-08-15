#!/usr/bin/env python
# coding: utf-8

import os
import re

import logging         # for logging mode/level
import argparse        # for command line usage (with options/arguments)
#import argparse_parent_with_group

# Local Import
from linuxiso.ressources.tools import run_cmd


class Virtualbox(object):
    """
    Class manage virtualbox with VBoxManage command

    The typical use is:
     - chose a config that containt all info about iso
     - **list** iso managed
     - get the **status** of one or all iso (**status_all**)
     - do operation on iso like **download**, **download_all**,
       **remove** or **remove_all**

    >>> virtualbox = Virtualbox(conf)
    >>> virtualbox.list_vms()
    >>> download.status("debian-9.5.0-strech-amd64-netinst.iso")
    >>> download.download("debian-9.5.0-strech-amd64-netinst.iso")

    """

    def __init__(self, conf=None):
        self.conf = conf

    @staticmethod
    def list_vms():
        """
        Get list vms
        return l_vm : dict result
        """
        logging.info('Get list vms')
        # == Command
        l_vm_raw = run_cmd('VBoxManage list vms ')
        l_vm = {}

        # == Extract information with RegEX
        regex = r"^\"(?P<hostname>[\w ]+)\" +\{(?P<id>[0-9a-f-]+)\}"
        for ligne in l_vm_raw.split('\n'):
            m = re.search(regex, ligne)
            if m:
                l_vm[m.group('hostname')] = m.group('id')

        return l_vm

    @staticmethod
    def list_ostypes():
        """
        Get list ostypes
        return l_ostypes : dict result
        """
        logging.info('Get list ostypes')
        # == Command
        l_ostypes_raw = run_cmd("VBoxManage list ostypes")
        l_ostypes = {}

        logging.debug('Extract information with RegEX')
        m_iter =re.finditer(r"ID:\s+(?P<id>\w*)\nDescription:\s+(?P<description>.*)\nFamily ID:\s+(?P<family_id>.*)\nFamily Desc:\s+(?P<family_desc>.*)\n64 bit:\s+(?P<b_64_bit>.*)",l_ostypes_raw,re.MULTILINE)

        for match in m_iter:
            l_ostypes[match.group("id")] = {
                "description": match.group("description"),
                "family_id":   match.group("family_id"),
                "family_desc": match.group("family_desc"),
                "b_64_bit":    match.group("b_64_bit")}

        return l_ostypes

    @staticmethod
    def get_machine_folder():
        """Get machine folder"""
        logging.info('Get machine folder')
        ligne = run_cmd("VBoxManage list systemproperties | grep \"Default machine folder:\"")

        logging.debug('Extract information with RegEX')
        m = re.search(r"^[^:]+:\s*(?P<dir_vm>.*)$", ligne)
        return m.group("dir_vm")
        #Default machine folder:          /home/jnaud/VirtualBox VMs

    @staticmethod
    def run(hostname):
        """ Run existing vm"""
        logging.info('Run existing vm')
        run_cmd("VBoxManage startvm "+hostname)

    def create(self, hostname, recipe, iso):
        """Create virtualbox vm"""
        logging.info('Create virtualbox vm')
        l_vm = self.list_vms()

        assert hostname not in l_vm.keys(), "Error : la vm '"+hostname+"' existe déjà"

        assert recipe in self.conf['virtualbox']['recipes'].keys(), "Error : la recipe '"+recipe+"' n'existe pas"

        #        dir1 = conf['disk-dir']+'/'+conf['hostname']
        #assert(not os.path.exists(dir1)), "Le dossier "+dir1+" existe déjà !"

        dir_iso = self.conf['dir_input']['path']
        dir_isocustom  = self.conf['dir_isocustom']['path']
        os_type = self.conf['virtualbox']['recipes'][recipe]['os_type']
        file_disk_type = self.conf['virtualbox']['recipes'][recipe]['file_disk_type']
        ram = str(self.conf['virtualbox']['recipes'][recipe]['ram'])
        vram = str(self.conf['virtualbox']['recipes'][recipe]['vram'])
        disk_size = self.conf['virtualbox']['recipes'][recipe]['disk_size']
        interface_name = self.conf['virtualbox']['recipes'][recipe]['interface_name']
        interface_type = self.conf['virtualbox']['recipes'][recipe]['interface_type']

        dir_vm = self.get_machine_folder()
        os.chdir(dir_vm)

        os.mkdir(dir_vm+os.sep+hostname)
        os.chdir(dir_vm+os.sep+hostname)

        # Create vm
        run_cmd(
            'VBoxManage createvm '
            '--name "'+hostname+'" '
            '--ostype "'+os_type+'" '  # Ex: "Debian_64"
            '--register')

        # Add SATA controller
        run_cmd(
            'VBoxManage storagectl "'+hostname+'" '
            '--name "SATA Controller" '
            '--add sata '
            '--controller IntelAHCI')

        # Add disks SATA controller
        if isinstance(disk_size, int):
            disk_size = [disk_size]
        run_cmd(
            'VBoxManage storagectl '+hostname+' '
            '--name "SATA Controller" '
            '--portcount '+str(len(disk_size)))  # Number of disque

        i = 0
        for on_disk_size in disk_size:
            ds = str(on_disk_size)
            it = str(i)
            disk_name = hostname+'_'+it+'.'+file_disk_type

            # Create one disk
            run_cmd(
                'VBoxManage createhd '
                '--filename "'+disk_name+'" '  # Ex:test_0.vmdk
                '--size '+ds)  # Disk size in Mo

            # Attach one disk to SATA controller
            run_cmd(
                'VBoxManage storageattach "'+hostname+'" '
                '--storagectl "SATA Controller" '
                '--port '+it+' '
                '--device 0 '
                '--type hdd '
                '--medium "'+disk_name+'"')  # Ex:test_0.vmdk
            i += 1

        # Add IDE Controller
        run_cmd(
            'VBoxManage storagectl "'+hostname+'" '
            '--name "IDE Controller" '
            '--add ide')

        # Mount the iso to the IDE controller
        run_cmd(
            'VBoxManage storageattach "'+hostname+'" '
            '--storagectl "IDE Controller" '
            '--port 0 '
            '--device 0 '
            '--type dvddrive '
            '--medium "'+iso+'"')

        # Enable Input/Output (mouse, keyboard, ...)
        run_cmd(
            'VBoxManage modifyvm  "'+hostname+'" '
            '--ioapic on')

        # Define boot order
        run_cmd(
            'VBoxManage modifyvm  "'+hostname+'" '
            '--boot1 dvd '
            '--boot2 disk '
            '--boot3 none '
            '--boot4 none')

        # Define RAM and VRAM(video)
        run_cmd(
            'VBoxManage modifyvm  "'+hostname+'" '
            '--memory '+ram+' '
            '--vram '+vram)

        # Connect network bridge interface
        run_cmd(
            'VBoxManage modifyvm  "'+hostname+'" '
            '--nic1 bridged '
            '--bridgeadapter1 '+interface_name)

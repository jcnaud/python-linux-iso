#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import re
import json
import yaml
from jsonschema import validate

import logging         # for logging mode/level
import argparse        # for command line usage (with options/arguments)
#import argparse_parent_with_group

class Virtualbox(object):
    """
    Class manage virtualbox with VBoxManage command
    """
    def __init__(self, conf_file="settings.yaml", conf=None):
        self.conf = self._load_conf(conf_file)
        pass

    def _load_conf(self, conf_file, conf=None):
        """
        Load & check configuration
        """
        if conf:
            conf_not_valided = conf
        else:
            with open(conf_file, "r") as f:
                conf_not_valided = yaml.load(f)
        
        with open("linuxiso_jsonschema.json", "r") as f:
            dict_schema = json.load(f)

        # If no exception, the conf is valided
        validate(conf_not_valided, dict_schema)
        return conf_not_valided

        # dict_schema = {
        #     'recipes': {
        #         And(str, len): {   # unique identifier
        #             'os_type': And(str, lambda s: s in self.get_list_ostypes().keys()),
        #             'file_disk_type':And(str,Use(str.lower),lambda s: s in ('vdi', 'vmdk')),
        #             'ram': And(Use(int), lambda n: 0 < n),
        #             'vram': And(Use(int), lambda n: 0 < n),
        #             'disk_size': And(Use(int), lambda n: 0 < n),
        #             'interface_name': And(str, len),
        #             'interface_type': And(str,Use(str.lower),lambda s: s in ('bridge', 'nat'))
        #         }
        #     },
        #     'dir_save': {
        #         'path': And(str, len)
        #     },
        #     'dir_isocustom': {
        #         'path': And(str, len)
        #     }
        # }

        # schema = Schema(dict_schema)
        # return schema.validate(conf_not_valided)
    
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
    def get_list_vms():
        """
        Get list vms
        return l_vm : dict result
        """
        logging.info('Get list vms')
        # == Command
        l_vm_raw = Virtualbox.run_cmd('VBoxManage list vms ')
        l_vm = {}

        # == Extract information with RegEX
        for ligne in l_vm_raw.split('\n'):
            m = re.search(r"^\"(?P<hostname>[\w ]+)\" +\{(?P<id>[0-9a-f-]+)\}", ligne)
            if m:
                l_vm[m.group('hostname')] = m.group('id')

        return l_vm

    @staticmethod
    def get_list_ostypes():
        """
        Get list ostypes
        return l_ostypes : dict result
        """
        logging.info('Get list ostypes')
        # == Command
        l_ostypes_raw = Virtualbox.run_cmd("VBoxManage list ostypes")
        l_ostypes = {}

        logging.debug('Extract information with RegEX')
        m_iter =re.finditer(r"ID:\s+(?P<id>\w*)\nDescription:\s+(?P<description>.*)\nFamily ID:\s+(?P<family_id>.*)\nFamily Desc:\s+(?P<family_desc>.*)\n64 bit:\s+(?P<b_64_bit>.*)",l_ostypes_raw,re.MULTILINE)

        for match in m_iter:
            l_ostypes[match.group("id")] = {
                "description" : match.group("description"),
                "family_id"   : match.group("family_id"),
                "family_desc" : match.group("family_desc"),
                "b_64_bit"    : match.group("b_64_bit")}

        return l_ostypes


    @staticmethod
    def get_machine_folder():
        """Get machine folder"""
        logging.info('Get machine folder')
        ligne = Virtualbox.run_cmd("VBoxManage list systemproperties | grep \"Default machine folder:\"")
        
        logging.debug('Extract information with RegEX')
        m = re.search(r"^[^:]+:\s*(?P<dir_vm>.*)$", ligne)
        return m.group("dir_vm")
        #Default machine folder:          /home/jnaud/VirtualBox VMs
        
    @staticmethod
    def run(hostname):
        """ Run existing vm"""
        logging.info('Run existing vm')
        Virtualbox.run_cmd("VBoxManage startvm "+hostname)



    def create(self, hostname, recipe, iso):
        """Create virtualbox vm"""
        logging.info('Create virtualbox vm')
        l_vm = self.get_list_vms()

        assert hostname not in l_vm.keys(), "Error : la vm '"+hostname+"' existe déjà"

        assert recipe in self.conf['virtualbox']['recipes'].keys(), "Error : la recipe '"+recipe+"' n'existe pas"

        #        dir1 = conf['disk-dir']+'/'+conf['hostname']
        #assert(not os.path.exists(dir1)), "Le dossier "+dir1+" existe déjà !"

        dir_iso        = self.conf['dir_save']['path']
        dir_isocustom  = self.conf['dir_isocustom']['path']
        os_type        = self.conf['virtualbox']['recipes'][recipe]['os_type']
        file_disk_type = self.conf['virtualbox']['recipes'][recipe]['file_disk_type']
        ram            = str(self.conf['virtualbox']['recipes'][recipe]['ram'])
        vram           = str(self.conf['virtualbox']['recipes'][recipe]['vram'])
        disk_size      = str(self.conf['virtualbox']['recipes'][recipe]['disk_size'])
        interface_name = self.conf['virtualbox']['recipes'][recipe]['interface_name']
        interface_type = self.conf['virtualbox']['recipes'][recipe]['interface_type']

        dir_vm = self.get_machine_folder()
        os.chdir(dir_vm)

        os.mkdir(dir_vm+os.sep+hostname)
        os.chdir(dir_vm+os.sep+hostname)
        #       VBoxManage createhd --filename "test_debian_manuel.vmdk"         --size 32768
        self.run_cmd('VBoxManage createhd --filename "'+hostname+'.'+file_disk_type+'" --size '+disk_size)

        #       VBoxManage createvm --name test_debian_manuel     --ostype "Debian_64"           --register
        self.run_cmd('VBoxManage createvm --name "'+hostname+'" --ostype "'+os_type+'" --register')

        #       VBoxManage storagectl "test_debian_manuel"   --name "SATA Controller" --add sata --controller IntelAHCI
        self.run_cmd('VBoxManage storagectl "'+hostname+'" --name "SATA Controller" --add sata --controller IntelAHCI')

        #       VBoxManage storageattach "test_debian_manuel"   --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium test_debian_manuel.vmdk
        self.run_cmd('VBoxManage storageattach "'+hostname+'" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "'+hostname+'.'+file_disk_type+'"')

        #       VBoxManage storagectl "test_debian_manuel"   --name "IDE Controller" --add ide
        self.run_cmd('VBoxManage storagectl "'+hostname+'" --name "IDE Controller" --add ide')

        #       VBoxManage storageattach "test_debian_manuel"   --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium /mnt2/data/var/debian-9.1.0-amd64-netinst.iso
        self.run_cmd('VBoxManage storageattach "'+hostname+'" --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "'+iso+'"') 

        #       VBoxManage modifyvm  "test_debian_manuel"   --ioapic on
        self.run_cmd('VBoxManage modifyvm  "'+hostname+'" --ioapic on')

        #       VBoxManage modifyvm  "test_debian_manuel"   --boot1 dvd --boot2 disk --boot3 none --boot4 none
        self.run_cmd('VBoxManage modifyvm  "'+hostname+'" --boot1 dvd --boot2 disk --boot3 none --boot4 none')


        #       VBoxManage modifyvm  "test_debian_manuel"   --memory 1024 --vram 128
        self.run_cmd('VBoxManage modifyvm  "'+hostname+'" --memory '+ram+' --vram '+vram)

        #       VBoxManage modifyvm  "test_debian_manuel"   --nic1 bridged --bridgeadapter1 enp3s0
        self.run_cmd('VBoxManage modifyvm  "'+hostname+'" --nic1 bridged --bridgeadapter1 '+interface_name)


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
            vb = Virtualbox(conf_file=args.config_file)
        else:
            vb = Virtualbox()

        # Manage "list", "create", "run" and "delete" options
        if args.list:             # List custom iso/image status
            result = vb.get_list_vms()
            print(json.dumps(result, indent=4))
        elif args.create:         # Create one VM
            vb.create(hostname=args.create, 
                recipe=args.recipe,
                iso=args.iso)
        elif args.run:            # Run one existing VM
            vb.run(args.run)
        elif args.delete:         # Delete one existing VM
            vb.delete(args.delete)
    
    # logging.basicConfig(level=logging.DEBUG)
    # #logger = logging.getLogger(__name__)

    # logging.getLogger(__name__).addHandler(logging.NullHandler())

    # #logger.info('Start create virtualbox vm')

    # vi = Virtualbox()
    
    # #l_vm = vi.get_list_vms()
    # #print(l_vm)

    # vi.create_vms(hostname="testdeploy",recipe="Debian-amd64-standard", iso="/home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso")
    # vi.run_vm("testdeploy")

    # #print(vi.get_list_ostypes())

    # #print(vi.get_machine_folder())
    # #vi.create("test_deb_1","Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso")


if __name__ == "__main__":
    """Entry point for command ligne usage (with options/arguments)"""


    parser_c = argparse.ArgumentParser("create",add_help=False)
    parser_c.add_argument("-i", "--iso", 
        help="iso/image to mount",
        metavar="ISO_NAME")
    parser_c.add_argument("-e", "--recipe", 
        help="recipe",
        metavar="RECIPE")


    parser = argparse.ArgumentParser(
        description='Program manage virtualbox VM',
        parents=[parser_c])


    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--list", 
        help="list curent VMs status", 
        action="store_true")   
    group.add_argument("-c", "--create", 
        help="create new VM (and mount an iso/image)",
        metavar="VM_NAME")
    group.add_argument("-r", "--run", 
        help="run virtualbox VM",
        metavar="VM_NAME")
    group.add_argument("-d", "--delete", 
        help="delete VM",
        metavar="VM_NAME")

    
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
    #   python virtualbox.py -l
    #   python virtualbox.py -c testdeploy -e Debian-amd64-standard -i /home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso
    #   python virtualbox.py -r testdeploy


#!/usr/bin/env python
# coding: utf-8

import logging
import logging.config
import os
import json
import yaml
from jsonschema import validate

from download   import Download
from custom     import Custom
from virtualbox import Virtualbox


def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)



class LinuxIso(object):
    """
    Class all the package linuxiso
    """
    def __init__(self,conf_file="settings.yaml"):
        
        self.conf = self._load_conf(conf_file)

        self.download  =   Download(conf=self.conf)
        self.custom    =     Custom(conf=self.conf)
        self.vitualbox = Virtualbox(conf=self.conf)


    def _load_conf(self, conf_file):
        """
        Load & check configuration
        :param conf_file : fichier de configuration
        :return : configuration valided
        """
        with open(conf_file, "r") as f:
            conf = yaml.load(f)
        
        with open("linuxiso_jsonschema.json", "r") as f:
            dict_schema = json.load(f)

        # If no exception, the conf is valided
        validate(conf, dict_schema)
        return conf


        
def main():
    setup_logging()
    li = LinuxIso()

    li.download.download("debian-9.2.1-strech-amd64-netinst.iso")
    li.custom.convert_iso("Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso")
    li.vitualbox.create_vms(hostname="testdeploy",recipe="Debian-amd64-standard", iso="/home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso")
    li.vitualbox.run_vm("testdeploy")

    
    #dl = Download()

    #vi = Virtualbox()
    #print(vi.get_list_vms())

    #vi.run_cmd("VBoxManage sldkjgfdlmjgsqjg<k")


if __name__ == "__main__":
    main()

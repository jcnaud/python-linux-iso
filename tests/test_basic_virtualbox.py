#!/usr/bin/env python
# coding: utf-8

import os
import sys
import pytest
import pyroute2
import uuid

try:
    # Package Import
    from linuxiso.virtualbox import Virtualbox  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa
except Exception:
    # Local import
    DIR_PWD = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(DIR_PWD, ".."))
    from linuxiso.virtualbox import Virtualbox  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa


@pytest.fixture
def custom_config(tmpdir):
    dirIso = tmpdir.mkdir("iso")
    dirIsoCustom = tmpdir.mkdir("isocustom")
    dirBuild = tmpdir.mkdir("build")
    test1 = dirIso.join("test_1.iso")
    test1.write("data on test_1")
    test2 = dirIso.join("test_2.iso")
    test2.write("data on test_2")

    # Get default iface name
    ip = pyroute2.IPDB()
    default_iface = ip.interfaces[ip.routes['default']['oif']]['ifname']
    ip.release()

    customConfig = {
        "general":{
            "dir_input": str(dirIso.realpath()),
            "dir_isocustom": str(dirIsoCustom.realpath()),
            "dir_build": str(dirBuild.realpath())
        },
        "download": {},
        "custom": {},
        "virtualbox": {
            "recipes": {
                "Debian-amd64-standard": {
                    'os_type': 'Debian_64',   # os type. => self.list_ostypes()
                    'file_disk_type': 'vmdk',  # vdi or vmdk
                    'ram': 1024,             # multiple of x^2 : example 1*1024
                    'vram': 128,             # video memory
                    'disk_size': 32768,      # multiple of x^2 : example 8*1024
                    'interface_name': default_iface,  # network interface used
                    'interface_type': 'bridged'
                }
            }
        }
    }
    return customConfig


def test_list_vms_with_custom_configuration(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    virtualbox = Virtualbox(conf=conf)
    result = virtualbox.list_vms()

    assert isinstance(result, list)


def test_list_ostypes(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    virtualbox = Virtualbox(conf=conf)
    result = virtualbox.list_ostypes()

    assert isinstance(result, dict)


def test_get_machine_folder(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    virtualbox = Virtualbox(conf=conf)
    result = virtualbox.get_machine_folder()

    assert result
    assert isinstance(result, str)


def test_create_and_remove(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    virtualbox = Virtualbox(conf=conf)
    hostname = 'test_'+str(uuid.uuid4())

    virtualbox.create(
        hostname=hostname,
        recipe='Debian-amd64-standard')

    virtualbox.remove(hostname)

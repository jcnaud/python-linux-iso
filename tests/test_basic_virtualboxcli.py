#!/usr/bin/env python
# coding: utf-8

import os
import sys
import six
import subprocess
import json
import yaml
import pytest
import pyroute2

# Local import
DIR_PWD = os.path.dirname(os.path.realpath(__file__))
DIR_PROGRAM = os.path.join(DIR_PWD, '..', 'scripts')
PROGRAM = os.path.join(DIR_PROGRAM, 'virtualboxcli')

@pytest.fixture
def custom_config_file(tmpdir):
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

    p = tmpdir.mkdir("conf").join("settings.yaml")
    p.write(yaml.dump(customConfig))

    return str(p.realpath())


def run_cmd(cmd, raseit=False, cwd=None):
    """
    Run a command
    if error, print and raise it
    params cmd : String commande
    return out
    """
    try:
        process = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        process.check_returncode()
    except Exception as e:
        if raseit:
            print(
                str(e)
                + "\nCMD_SHELL : "+cmd
                + "\nSTDOUT : "+process.stdout.decode()
                + "\nSTDERR : "+process.stderr.decode(),
                exc_info=True)
        else:
            six.reraise(*sys.exc_info())

    return process.stdout.decode()


def test_help():
    """Test help option"""
    cmd = PROGRAM+' --help'
    result = run_cmd(cmd, cwd=DIR_PROGRAM)

    # Compare result
    assert result


def test_list(custom_config_file):
    """Test list option"""
    cmd = PROGRAM+' --config '+custom_config_file+' --list'
    result = run_cmd(cmd, cwd=DIR_PROGRAM)

    # Compare result
    assert isinstance(json.loads(result), list)


def test_list_ostype(custom_config_file):
    """Test list option"""
    cmd = PROGRAM+' --config '+custom_config_file+' --list-ostype'
    result = run_cmd(cmd, cwd=DIR_PROGRAM)

    # Compare result
    assert json.loads(result)

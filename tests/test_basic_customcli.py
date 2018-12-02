#!/usr/bin/env python
# coding: utf-8

import os
import sys
import six
import subprocess
import json
import yaml
import pytest

# Local import
DIR_PWD = os.path.dirname(os.path.realpath(__file__))
DIR_PROGRAM = os.path.join(DIR_PWD, '..', 'scripts')
PROGRAM = os.path.join(DIR_PROGRAM, 'customcli')

@pytest.fixture
def custom_config_file(tmpdir):
    dirIso = tmpdir.mkdir("iso")
    dirIsoCustom = tmpdir.mkdir("isocustom")
    dirBuild = tmpdir.mkdir("build")
    test0 = dirIso.join("test_0.iso")
    test0.write("data on test_0")

    customConfig = {
        "general": {
            "dir_input": str(dirIso.realpath()),
            "dir_isocustom": str(dirIsoCustom.realpath()),
            "dir_build": str(dirBuild.realpath()),
        },
        "download": {
            "test_0.iso": {  # Downloaded and good hash
                "label": "test the iso",
                "url_iso": "https://test.com/test_0.iso",
                "hash": {
                    "type": "sha1",
                    "sum": test0.computehash(
                        hashtype="sha1",
                        chunksize=65536)
                }
            },
        },
        "custom": {
            "iso": {
                "test_custom_0.iso": {
                    "receipt": "Custom-FullAuto-Debian-9-strech-amd64-netinst-server",
                    "vars":{
                        "hostname": "test_custom_0",      # <Unique hostnamename>
                        "domain": "example.lan",           # <Domaine name>
                        "var_ntp_server": "pool.ntp.org",  # <NTP serveur> for time synchronisation
                        "root_password": "mypassword",     # <root password>
                        "user_name": "myuser",             # <user name>
                        "user_password": "mypassword"     # <user password>
                    }
                },
                "test_custom_1.iso": {
                    "receipt": "Custom-FullAuto-Debian-9-strech-amd64-netinst-server",
                    "vars":{
                        "hostname": "test_custom_1",      # <Unique hostnamename>
                        "domain": "example.lan",           # <Domaine name>
                        "var_ntp_server": "pool.ntp.org",  # <NTP serveur> for time synchronisation
                        "root_password": "mypassword",     # <root password>
                        "user_name": "myuser",             # <user name>
                        "user_password": "mypassword"     # <user password>
                    }
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
    assert json.loads(result)

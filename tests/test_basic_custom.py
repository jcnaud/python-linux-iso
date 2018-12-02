#!/usr/bin/env python
# coding: utf-8

import os
import sys
import requests_mock
import pytest

try:
    # Package Import
    from linuxiso.custom.core import Custom  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa
except Exception:
    # Local import
    DIR_PWD = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(DIR_PWD, ".."))
    from linuxiso.custom.core import Custom  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa

requests_mock.mock.case_sensitive = True


@pytest.fixture
def custom_config(tmpdir):
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

    return customConfig


def test_list_with_custom_configuration(custom_config):
    # Run test
    conf = load_conf(confDict=custom_config)  # Custom configuration
    custom = Custom(conf=conf)
    result = custom.list()

    # Compare result
    excepted = ['test_custom_0.iso']
    assert result.sort() == excepted.sort()


def test_status_iso_not_create(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    custom = Custom(conf=conf)
    result = custom.status('test_custom_0.iso')

    expected = {
        'is_exist': False
    }

    assert result == expected

#!/usr/bin/env python
# coding: utf-8

import os
import sys
#import requests
import requests_mock

try:
    # Package Import
    from linuxiso.download import Download  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa
except Exception:
    # Local import
    DIR_PWD = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(DIR_PWD, ".."))
    from linuxiso.download import Download  # noqa
    from linuxiso.ressources.tools import load_conf  # noqa

requests_mock.mock.case_sensitive = True

customConf = {
    "dir_input": {
        "path": "/home/jnaud/var/iso"
    },
    "dir_isocustom": {
        "path": "/home/jnaud/var/isocustom"
    },
    "dir_build": {
        "path": "/home/jnaud/var/build"
    },
    "download": {
        "test.iso": {
            "label": "test the iso",
            "url_iso": "https://test.com/test.iso",
            "hash": {
                "type": "sha1",
                "sum": "ed1cf0dea20831fb26661c10ca65340e3a3ea616"
            }
        }
    }
}


def test_download_list_with_default_configuration():
    conf = load_conf()  # Load default configuration
    download = Download(conf=conf)
    result = download.list()
    assert len(result) != 0


def test_download_list_with_custom_configuration():
    conf = load_conf(confDict=customConf)  # Custom configuration
    download = Download(conf=conf)
    result = download.list()

    excepted = list(customConf['download'].keys())
    assert result.sort() == excepted.sort()


def test_download_check_url_http_exception():
    with requests_mock.Mocker() as m:
        m.register_uri(
            'HEAD',
            'https://test.com/test.iso',
            exc=Exception)

        conf = load_conf(confDict=customConf)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test.iso')

        expected = {
            'is_url_exist': False,
            'is_downloaded': False
        }

        assert result == expected


def test_download_check_url_error_400():
    with requests_mock.Mocker() as m:
        m.register_uri(
            'HEAD',
            'https://test.com/test.iso',
            status_code=400)

        conf = load_conf(confDict=customConf)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test.iso')

        expected = {
            'is_url_exist': False,
            'is_downloaded': False
        }

        assert result == expected


def test_download_check_url_iso_not_downloaded():
    with requests_mock.Mocker() as m:
        m.head('https://test.com/test.iso')

        conf = load_conf(confDict=customConf)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test.iso')

        expected = {
            'is_url_exist': True,
            'is_downloaded': False
        }

        assert result == expected


def test_download_check_url_iso_downloaded(tmpdir):
    with requests_mock.Mocker() as m:
        m.head('https://test.com/test.iso')

        conf = load_conf(confDict=customConf)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test.iso')

        expected = {
            'is_url_exist': True,
            'is_downloaded': True
        }

        assert result == expected

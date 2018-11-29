#!/usr/bin/env python
# coding: utf-8

import os
import sys
import requests_mock
import pytest

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


@pytest.fixture
def custom_config(tmpdir):
    dirIso = tmpdir.mkdir("iso")
    dirIsoCustom = tmpdir.mkdir("isocustom")
    dirBuild = tmpdir.mkdir("build")
    test1 = dirIso.join("test_1.iso")
    test1.write("data on test_1")
    test2 = dirIso.join("test_2.iso")
    test2.write("data on test_2")

    customConfig = {
        "general":{
            "dir_input": str(dirIso.realpath()),
            "dir_isocustom": str(dirIsoCustom.realpath()),
            "dir_build": str(dirBuild.realpath())
        },
        "download": {
            "test_0.iso": {  # Not downloaded
                "label": "test the iso",
                "url_iso": "https://test.com/test_0.iso"
            },
            "test_1.iso": {  # Downloaded but wrong hash
                "label": "test the iso",
                "url_iso": "https://test.com/test_1.iso",
                "hash": {
                    "type": "sha1",
                    "sum": "WRONG_HASH"
                }
            },
            "test_2.iso": {  # Downloaded and good hash
                "label": "test the iso",
                "url_iso": "https://test.com/test_2.iso",
                "hash": {
                    "type": "sha1",
                    "sum": test2.computehash(
                        hashtype="sha1",
                        chunksize=65536)
                }
            },
            "test_3.iso": {  # To download
                "label": "test the iso",
                "url_iso": "https://test.com/test_3.iso",
                "hash": {
                    "type": "sha1",
                    "sum": test2.computehash(
                        hashtype="sha1",
                        chunksize=65536)
                }
            }
        }
    }
    return customConfig


@pytest.fixture
def file_to_download(tmpdir):
    test3 = tmpdir.join("test_3.iso")
    test3.write("data on test_2")

    return str(test3.realpath())


# def test_list_with_default_configuration():
#     conf = load_conf()  # Load default configuration
#     download = Download(conf=conf)
#     result = download.list()
#     assert len(result) != 0


def test_list_with_custom_configuration(custom_config):
    # Run test
    conf = load_conf(confDict=custom_config)  # Custom configuration
    download = Download(conf=conf)
    result = download.list()

    # Compare result
    excepted = ["test_0.iso", "test_1.iso", "test_2.iso", "test_3.iso"]
    assert result.sort() == excepted.sort()


def test_status_http_exception(custom_config):
    with requests_mock.Mocker() as m:
        m.register_uri(
            'HEAD',
            'https://test.com/test_0.iso',
            exc=Exception)

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test_0.iso')

        expected = {
            'is_url_exist': False,
            'is_downloaded': False
        }

        assert result == expected


def test_status_error_400(custom_config):
    with requests_mock.Mocker() as m:
        m.register_uri(
            'HEAD',
            'https://test.com/test_0.iso',
            status_code=400)

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test_0.iso')

        expected = {
            'is_url_exist': False,
            'is_downloaded': False
        }

        assert result == expected


def test_status_iso_not_downloaded(custom_config):
    with requests_mock.Mocker() as m:
        m.head('https://test.com/test_0.iso')

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test_0.iso')

        expected = {
            'is_url_exist': True,
            'is_downloaded': False
        }

        assert result == expected


def test_status_iso_downloaded_bad_hash(custom_config):
    with requests_mock.Mocker() as m:
        m.head('https://test.com/test_1.iso')

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test_1.iso')

        expected = {
            'is_url_exist': True,
            'is_downloaded': True,
            'is_hash_valid': False
        }
        assert result == expected


def test_status_iso_downloaded_good_hash(custom_config):
    with requests_mock.Mocker() as m:
        m.head('https://test.com/test_2.iso')

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        result = download.status('test_2.iso')

        expected = {
            'is_url_exist': True,
            'is_downloaded': True,
            'is_hash_valid': True
        }
        assert result == expected


def test_status_all(custom_config):
    with requests_mock.Mocker() as m:
        m.head('https://test.com/test_2.iso')

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        result = download.status_all()

        expected = {
            "test_0.iso": {
                "is_url_exist": False,
                "is_downloaded": False
            },
            "test_1.iso": {
                "is_url_exist": False,
                "is_downloaded": True,
                "is_hash_valid": False
            },
            "test_2.iso": {
                "is_url_exist": True,
                "is_downloaded": True,
                "is_hash_valid": True
            },
            "test_3.iso": {
                "is_url_exist": False,
                "is_downloaded": False
            }
        }
        assert result == expected


def test_download_iso_not_downloaded(custom_config, file_to_download):
    with requests_mock.Mocker() as m:
        with open(file_to_download) as file:
            m.get('https://test.com/test_3.iso', headers={'content-length': '29'}, body=file)

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        download.download('test_3.iso')

        result = os.path.isfile(
            os.path.join(
                custom_config['general']['dir_input'],
                'test_3.iso'))
        assert result


def test_download_iso_already_downloaded(custom_config, file_to_download):
    iso_path = os.path.join(
        custom_config['general']['dir_input'],
        'test_2.iso')
    init_timestamp = os.path.getmtime(iso_path)
    print(init_timestamp)
    with requests_mock.Mocker() as m:
        with open(file_to_download) as file:
            m.get('https://test.com/test_2.iso',  headers={'content-length': '29'}, body=file)

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        download.download('test_2.iso')

        result = os.path.getmtime(iso_path)
        expected = init_timestamp
        assert result == expected


def test_download_all(custom_config, file_to_download):
    with requests_mock.Mocker() as m:
        with open(file_to_download) as file:
            m.get('https://test.com/test_0.iso', headers={'content-length': '29'}, body=file)
            m.get('https://test.com/test_1.iso', headers={'content-length': '29'}, body=file)
            m.get('https://test.com/test_2.iso', headers={'content-length': '29'}, body=file)
            m.get('https://test.com/test_3.iso', headers={'content-length': '29'}, body=file)

        conf = load_conf(confDict=custom_config)  # Custom configuration
        download = Download(conf=conf)
        download.download_all()

        result = True
        for file_name in custom_config['download'].keys():
            file_path = os.path.join(
                custom_config['general']['dir_input'],
                file_name)
            if not os.path.isfile(file_path):
                result = False
        assert result


def test_remove_iso_not_downloaded(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    download = Download(conf=conf)
    result = download.remove('test_2.iso')

    result = os.path.isfile(
        os.path.join(
            custom_config['general']['dir_input'],
            'test_2.iso'))

    assert not result


def test_remove_iso_already_downloaded(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    download = Download(conf=conf)
    result = download.remove('test_2.iso')

    result = os.path.isfile(
        os.path.join(
            custom_config['general']['dir_input'],
            'test_2.iso'))

    assert not result


def test_remove_all_iso(custom_config):
    conf = load_conf(confDict=custom_config)  # Custom configuration
    download = Download(conf=conf)
    result = download.remove_all()

    result = True
    for file_name in custom_config['download'].keys():
        file_path = os.path.join(
            custom_config['general']['dir_input'],
            file_name)
        if os.path.isfile(file_path):
            result = False

    assert result

#!/usr/bin/env python
# coding: utf-8

import os
import requests
import hashlib  # Hash function
import logging  # for logging mode/level


class Download(object):
    """
    Class manage download and verify iso.

    :param dict conf: Configuration

    You need to provide configuration with all info of iso managed.

    The typical use is:
     - chose a config that containt all info about iso
     - **list** iso managed
     - get the **status** of one or all iso (**status_all**)
     - do operation on iso like **download**, **download_all**,
       **remove** or **remove_all**

    >>> download = Download(conf)
    >>> download.list()
    >>> download.status("debian-9.5.0-strech-amd64-netinst.iso")
    >>> download.download("debian-9.5.0-strech-amd64-netinst.iso")

    """

    def __init__(self, conf=None):
        self.conf = conf

    def list(self):
        """Get list of iso managed.

        :return: List of iso managed
        :rtype: list

        >>> download.list()
        [
            "centos-7-x86-amd64-desktop.iso",
            "debian-10-buster-amd64-netinst-testing.iso",
            "debian-9.5.0-strech-amd64-netinst.iso",
            "kde-18.3-destop-kde.iso",
            "linuxmint-18.2-Sonya-amd64-desktop-cinnamon.iso",
            "raspbian-9-strech-lite.img",
            "ubuntu-16.04.4-LTS-Xenial_Xerus-amd64-desktop-live.iso",
            "ubuntu-16.04.4-LTS-Xenial_Xerus-amd64-server.iso",
            "ubuntu-17.10.1-Artful_Aardvark-amd64-server.iso"
        ]

        """
        return sorted(list(self.conf['download'].keys()))

    def status(self, iso):
        """Get one iso status.

        :param str iso: Name of iso used
        :return: Status of the iso
        :rtype: dict

        Test :
         - if the url to download the iso exist
         - if the iso already downloaded
         - if the checksum is good (if the iso is download)

        >>> download.status("debian-9.5.0-strech-amd64-netinst.iso")
        {
            "is_downloaded": true,
            "is_hash_valid": true,
            "is_url_exist": true
        }

        """
        iso_params = self.conf['download'][iso]
        url = iso_params['url_iso']
        result = {}
        result['is_url_exist'] = self._check_url(url)

        file = os.path.join(self.conf['dir_input']['path'], iso)
        if os.path.isfile(file):
            result['is_downloaded'] = True

            if 'hash' in iso_params.keys():
                iso_hash = iso_params['hash']
                if iso_hash['type'] in hashlib.algorithms_available:
                    hasher = getattr(hashlib, iso_hash['type'])()
                    BLOCKSIZE = 65536
                    with open(file, 'rb') as afile:
                        buf = afile.read(BLOCKSIZE)
                        while len(buf) > 0:
                            hasher.update(buf)
                            buf = afile.read(BLOCKSIZE)
                    if iso_hash['sum'] == hasher.hexdigest():
                        result['is_hash_valid'] = True
                    else:
                        result['is_hash_valid'] = False
        else:
            result['is_downloaded'] = False

        return result

    def status_all(self):
        """Get all iso status.

        :return: status of all iso managed
        :rtype: dict

        Test if the url to download exist, if the iso already downloaded
        and if the checksum is good

        >>> download.status_all()
        """

        l_iso = self.conf['download']
        result = {}
        for iso in l_iso.keys():
            result[iso] = self.status(iso)
        return result

    def _check_url(self, url):
        """ Check if url exist

        :return: True if url exist, else False
        :rtype: bool
        """
        try:
            reponse = requests.head(url, allow_redirects=True)
            if reponse.status_code == 200:
                return True
        except Exception as e:
            logging.debug(e)

        return False

    def download(self, iso):
        """Download one iso

        :param str iso: Name of iso used

        >>> download.download("debian-9.5.0-strech-amd64-netinst.iso")
        """
        url_iso = self.conf['download'][iso]['url_iso']
        dir_input = self.conf['dir_input']['path']
        file_iso = dir_input+os.sep+iso

        if not os.path.isdir(dir_input):
            os.makedirs(dir_input)

        if not os.path.exists(file_iso):
            logging.info("Download : "+file_iso)
            # urllib.request.urlretrieve(url_iso, file_iso)
            rep = requests.get(url_iso, stream=True, allow_redirects=True)
            with open(file_iso, 'wb') as fd:
                for chunk in rep.iter_content(chunk_size=128):
                    fd.write(chunk)
        else:
            logging.info("File exist, do nothing because already downloaded")

    def download_all(self):
        """ Download all iso

        >>> download.download_all()
        """
        for i in self.conf['download'].keys():
            self.download(i)

    def remove(self, iso):
        """ Remove one iso

        :param str iso: Name of iso used

        >>> download.remove("debian-9.5.0-strech-amd64-netinst.iso")
        """
        file_iso = self.conf['dir_input']['path']+os.sep+iso
        if os.path.isfile(file_iso):
            os.remove(file_iso)

    def remove_all(self):
        """ Remove all iso

        >>> download.remove_all()
        """
        for iso in self.conf['download'].keys():
            self.remove(iso)

#!/usr/bin/env python
# coding: utf-8

# Local import
from linuxiso.download import Download
from linuxiso.custom.core import Custom
from linuxiso.virtualbox import Virtualbox
from linuxiso.ressources.tools import setup_logging, load_conf


class LinuxIso(object):
    """
    Linux iso class managed the chain
    """

    def __init__(self, conf_file=None):
        """Init by loading main configuration file"""
        self.conf = load_conf(conf_file)

        self.download = Download(conf=self.conf)
        self.custom = Custom(conf=self.conf)
        self.vitualbox = Virtualbox(conf=self.conf)


def main():
    """Enter point of this package"""
    setup_logging()
    li = LinuxIso()

    li.download.download("debian-9.6.0-strech-amd64-netinst.iso")

    context = {
        'ansible_user_name': 'ansible',
        'ansible_authorized_keys': [
            'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxxDwYctg2ngBkR5Xuzz3NxGIxqY88nOVP1SOnAz24B3LfCn7EzpEHvUC/Dw+fGk0CmFEQZMBFc7vjOTVT1kk2wajX241y+zHd92JA1NFdxa8T2kg5xlkXK5zAvs5a/PRmTcijnSK1ynw1t+uglLgpj3UkhZ3OScfc8xmb1SPy/8carF44HavNI0/KTXjyuBuM3b+9GXChwMLI2ZNQZ+RAEVH5nsaLwPqWVHCe6JID2ApIHNq4kC/V9pRGsH1w4tApVspCJ4lnSlMxVLbnS+zdJpV2/UpaFv64VG5KTbkeNYBwg7EE6KVI+bU93AMZYI75UeEPafWT/WESDW9K1RbH root@edugastp'
        ],
        'hostname': 'test',
        'domain': 'naud.lan',
        'var_ntp_server': 'mafreebox.free.fr',
        'root_password': 'tititoto',
        'user_name': 'jcnaud',
        'user_password': 'tititoto'
    }

    li.custom.create(
        "Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso",
        context)
    li.vitualbox.create(
        hostname="testdeploy",
        recipe="Debian-amd64-standard",
        iso="/home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso")

    li.vitualbox.run("testdeploy")
    # print(vi.get_list_vms())


if __name__ == "__main__":
    main()

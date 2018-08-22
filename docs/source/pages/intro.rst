************
Introduction
************

This program allow to :
 - download iso
 - custum iso
 - deploy on virtualbox an iso


Links
=====
source code : <https://github.com/jcnaud/python-linux-iso>





dd bs=4M if=2018-04-18-raspbian-stretch.img of=/dev/sdX status=progress conv=fsync


unzip -p 2018-04-18-raspbian-stretch.zip | sudo dd of=/dev/sdX bs=4M conv=fsync

sync

systemd-nspawn

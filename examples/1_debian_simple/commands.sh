#!/bin/bash

echo 'Download : list'
../../scripts/downloadcli --config settings.yaml --list

echo 'Download : status debian-9.5.0-strech-amd64-netinst.iso'
../../scripts/downloadcli --config settings.yaml --status debian-9.5.0-strech-amd64-netinst.iso

echo 'Download : download'
../../scripts/downloadcli --config settings.yaml --download debian-9.5.0-strech-amd64-netinst.iso

echo 'Custom : list'
../../scripts/customcli --config settings.yaml --list

echo 'Custom : status Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso'
../../scripts/customcli --config settings.yaml --status Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso

echo 'Custom : create Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso'
../../scripts/customcli --config settings.yaml --create Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso --context uniquehostname

echo 'Virtualbox : list'
../../scripts/virtualboxcli --config settings.yaml --list

echo 'Virtualbox : create uniquehostname'
../../scripts/virtualboxcli --config settings.yaml --create Debian-amd64-standard --iso Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso

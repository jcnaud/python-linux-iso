#!/bin/bash

echo 'Download : list'
../../scripts/downloadcli --config settings.yaml --list

echo 'Download : status debian-9.6.0-strech-amd64-netinst.iso'
../../scripts/downloadcli --config settings.yaml --status debian-9.6.0-strech-amd64-netinst.iso

echo 'Download : download'
../../scripts/downloadcli --config settings.yaml --download debian-9.6.0-strech-amd64-netinst.iso

echo 'Custom : list'
../../scripts/customcli --config settings.yaml --list

echo 'Custom : status myhostname.iso'
../../scripts/customcli --config settings.yaml --status myhostname.iso

echo 'Custom : create myhostname.iso'
../../scripts/customcli --config settings.yaml --create myhostname.iso

echo 'Virtualbox : list'
../../scripts/virtualboxcli --config settings.yaml --list

echo 'Virtualbox : create myhostname'
../../scripts/virtualboxcli --config settings.yaml --create myhostname

echo 'Virtualbox : run myhostname'
../../scripts/virtualboxcli --config settings.yaml --run myhostname

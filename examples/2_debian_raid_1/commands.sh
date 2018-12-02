#!/bin/bash

echo 'Download : list'
../../scripts/downloadcli --config settings.yaml --list

echo 'Download : status debian-9.6.0-strech-amd64-netinst.iso'
../../scripts/downloadcli --config settings.yaml --status debian-9.6.0-strech-amd64-netinst.iso

echo 'Download : download'
../../scripts/downloadcli --config settings.yaml --download debian-9.6.0-strech-amd64-netinst.iso

echo 'Custom : list'
../../scripts/customcli --config settings.yaml --list

echo 'Custom : status myhostname2.iso'
../../scripts/customcli --config settings.yaml --status myhostname2.iso

echo 'Custom : create myhostname2.iso'
../../scripts/customcli --config settings.yaml --create myhostname2.iso

echo 'Virtualbox : list'
../../scripts/virtualboxcli --config settings.yaml --list

echo 'Virtualbox : create myhostname2'
../../scripts/virtualboxcli --config settings.yaml --create myhostname2

echo 'Virtualbox : run myhostname2'
../../scripts/virtualboxcli --config settings.yaml --run myhostname2

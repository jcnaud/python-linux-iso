#!/bin/bash

echo 'Download : list'
../../scripts/downloadcli --config settings.yaml --list

echo 'Download : ubuntu-18-bionic-beaver-amd64-cd-server.iso'
../../scripts/downloadcli --config settings.yaml --status ubuntu-18-bionic-beaver-amd64-cd-server.iso

echo 'Download : download'
../../scripts/downloadcli --config settings.yaml --download ubuntu-18-bionic-beaver-amd64-cd-server.iso

echo 'Custom : list'
../../scripts/customcli --config settings.yaml --list

echo 'Custom : status myhostname-ubuntu-18-server.iso'
../../scripts/customcli --config settings.yaml --status myhostname-ubuntu-18-server.iso

echo 'Custom : create myhostname-ubuntu-18-server.iso'
../../scripts/customcli --config settings.yaml --create myhostname-ubuntu-18-server.iso

echo 'Virtualbox : list'
../../scripts/virtualboxcli --config settings.yaml --list

echo 'Virtualbox : create myhostname-ubuntu-18-server'
../../scripts/virtualboxcli --config settings.yaml --create myhostname-ubuntu-18-server

echo 'Virtualbox : run myhostname-ubuntu-18-server'
../../scripts/virtualboxcli --config settings.yaml --run myhostname-ubuntu-18-server

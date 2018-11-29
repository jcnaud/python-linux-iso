****************
Python linux iso
****************

.. inclusion-marker-do-not-remove

.. image:: https://readthedocs.org/projects/python-linux-iso/badge/?version=develop
    :target: https://python-linux-iso.readthedocs.io/en/latest/?badge=develop
    :alt: Documentation Status

.. image:: https://travis-ci.org/jcnaud/python-linux-iso.svg?branch=develop
    :target: https://travis-ci.org/jcnaud/python-linux-iso


.. image:: https://api.codeclimate.com/v1/badges/9fab9605801e7de8c05e/maintainability
   :target: https://codeclimate.com/github/jcnaud/python-linux-iso/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/9fab9605801e7de8c05e/test_coverage
    :target: https://codeclimate.com/github/jcnaud/python-linux-iso/test_coverage
    :alt: Test Coverage

Resume
======

This programme provide a way to **download**, **custom** and **deploy**, full **automatically**, an OS ISO.
The second goal of this project is to never use linux root access to make this.

This programme have **tree** modules:
 - download
 - custom
 - virtualbox
 - (FUTURE DEVELOPPEMENT) pxe

Actually, you can custom this offical ISO:
 - debian 9
 - unbuntu 16 (UNDER DEVELOPPEMENT)
 - unbuntu 17 (UNDER DEVELOPPEMENT)

Each module can be use independently in different way like:
 - Command Line Interface (CLI)
 - python module

This programme is run with python:
 - 3.6 (UNDER DEVELOPPEMENT)
 - 3.5

Getting started
===============

Use configuration file, many of them are in **examples** directory.
For example, use **examples/1_debian_simple/settings.yml**

Change **General** parameters to avoid warning about using default directories:
- general.dir_input: <directory where offical iso are>
- general.dir_isocustom: <directory to put custom iso>
- general.dir_build: <temp directory where we build iso>


Now typical work flow is:

Download debian ISO::

  cd example/1_debian_simple
  ../../scripts/downloadcli --config settings.yaml --download debian-9.6.0-strech-amd64-netinst.iso

Custom this debian iso with recipe::

  ../../scripts/customcli --config settings.yaml --create Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso --context ./example/debiansimple/context.yaml

Deploy on virtualbox::

  ../../scripts/virtualboxcli --config settings.yaml --create Debian-amd64-standard --iso Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso


You have more commands examples in **examples/1_debian_simple/commands.sh** and you can run it with::

  cd example/1_debian_simple
  ./commands.sh

Or deploy on USB KEY (cf. documentation)

Or deploy on PXE (FUTURE DEVELOPPEMENT)


Architecture
============

Life cycle:
 - Download
 - Custom
 - Deploy
    - on usb key
    - on localhost vitualbox
    - on localhost PXE (FUTURE DEVELOPPEMENT)

Project structure::

  ├── docs/            # Sphinx documentation deploy on **readthedoc.io**
  ├── examples/
  ├── linuxiso/        # Source code
  │   ├── __init__.py
  │   ├── __main__.py
  │   ├── conf/
  │   ├── download.py    # Download module part
  │   ├── custom/        # Custom module part
  │   ├── virtualbox.py  # Vituralbox module part
  │   ├── ressources     # Generique function (Ex: logging, load conf, ...)
  │   └── scripts        # Code for command line interface support for all modules
  ├── scripts/  # User entry point for command line interface for all modules
  ├── tests/    # Test (pytest+coverage) deployed on **travis-ci.org** and **codeclimate.com**
  │
  ├── README.rst
  ├── LICENSE.txt
  ├── requirements-dev.txt # Python dependencies for develop (build doc, run tests, ...)
  ├── requirements.txt     # Python dependencies for production
  └── setup.py


Installation
============

This programme works only on **linux distribution** because he use bash command.

To avoid using root access, we need some tools for mount, unmount and build ISO.

Linux package
-------------
For example, on debian, install theses paquages

```bash
sudo apt-get install xorriso virtualbox
```

Python
------
A strongly advice you to use **virtualenv**.

Install virtualenv::

  sudo apt-get install virtualenv

  cd python-linux-iso/
  virtualenv -p /usr/bin/python3 venv
  source venv/bin/activate
  pip install -t requirements.txt
  deactivate

  pip install module
  python setup.py install



Run unit test
=============

First install developpement dependency::

  pip install -r requirements-dev.txt

Secondly, execute all test using **pytest**::

  pytest tests


Compile documentation
=====================
This documentation is generated with sphinx.

First install developpement dependency::

  pip install -r requirements-dev.txt

Secondly, compile the documentation with sphinx::

  cd docs
  make html

The entry point of the documentation is in **docs/build/html/index.html**.


Compile distribution package (UNDERDEVELOPPEMENT)
=================================================

Compile distribution package from source::

  python setup.py sdist

The distribution package are in the **dist** directory


Run tests with coverage
=======================
The calcul of tests coverage is make with **pytest-cov**.

First install developpement dependency::

  pip install -r requirements-dev.txt

Run tests with coverage::

  py.test --cov=linuxiso tests


Links
=====
Debian wiki for Raspbian: https://wiki.debian.org/RaspberryPi/qemu-user-static
Mount all king of *.img: https://www.suse.com/c/accessing-file-systems-disk-block-image-files/

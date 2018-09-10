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

Project structure
=================

::

  ├── docs/            # Sphinx documentation deploy on **readthedoc.io**
  ├── examples/
  ├── linuxiso/        # Source code
  │   ├── __init__.py
  │   ├── __main__.py
  │   ├── conf/
  │   ├── download.py    # Download module part
  │   ├── custom/        # Custom module part
  │   ├── virtualbox.py  # Vituralbox module part
  │   ├── ressources     # Generique function (Ex: log, load conf, ...)
  │   └── scripts        # Code command line terminal support for all modules
  ├── scripts/  # Entry point for command line terminal for all modules
  ├── tests/    # Test (pytest+coverage) deployed on **travis-ci.org** and **codeclimate.com**
  │
  ├── README.rst
  ├── LICENSE.txt
  ├── requirements-dev.txt # Python dependencies for develop
  ├── requirements.txt     # Python dependencies for production
  └── setup.py


Deploy an iso or custom iso on USB key
======================================


 - First, you need USB key clean dan formated in FAT32
 - Secondly, find the USB key dev (Ex: /dev/sdb or /deb/sdc, ...). ATTENTION, if you chose the wrong dev, you can errase your disk.::

  sudo dd bs=4M if=./input.iso of=/dev/sdX status=progress conv=fsync


Where ./input.iso is the iso selected to deplay on USB and /dev/sdX is the USB key dev

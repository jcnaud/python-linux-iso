****************
Python linux iso
****************

.. image:: https://travis-ci.org/jcnaud/python-linux-iso.svg?branch=master
    :target: https://travis-ci.org/jcnaud/python-linux-iso


.. image:: https://api.codeclimate.com/v1/badges/9fab9605801e7de8c05e/maintainability
   :target: https://codeclimate.com/github/jcnaud/python-linux-iso/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/9fab9605801e7de8c05e/test_coverage
    :target: https://codeclimate.com/github/jcnaud/python-linux-iso/test_coverage
    :alt: Test Coverage


Links
=====

Online documentation : TODO


Overviews
=========

This programme provide a way to **deploy**, full **automatically**, an OS from ISO.
The second goal of this project is to never use linux root access to make this.

This programme have **three** parts:

 - download
 - custom
 - virtual box

Actually, you can custom:

 - debian 9
 - unbuntu 16 (UNDER DEV)
 - unbuntu 17 (UNDER DEV)

Each part can be use independently in different way like:
 - Command Line Interface (CLI)
 - python module

This programme use python 3.5.4+

Installation
============

This programme works only on **linux distribution** because he use bash command.

To avoid using root access, we need some tools for mount, unmount and build iso.

Linux package
-------------
For example, on debian, install theses paquages
```bash
apt-get install xorriso virtualbox
```
Python
------
This programme use python 3.5.4+
A strongly advice you to use **virtualenv**.

Install virtualenv
```bash
apt-get install virtualenv
```

Mouv to the directory of the project and create virtualenv::
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


Compile distribution package
============================

Compile distribution package from source::

    python setup.py sdist

The distribution package are in the **dist** directory


Calcul tests coverage
=====================
The calcul of tests coverage is make with **pytest-cov**.

First install developpement dependency::

    pip install -r requirements-dev.txt

Run coverage::

     py.test --cov=linuxiso tests

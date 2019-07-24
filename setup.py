# coding: utf-8
import os
import linuxiso    # Used to get the version on the __init__.py
from setuptools import setup, find_packages

"""
Read description file
"""
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='LinuxIso',

    python_requires='>=3',
    install_requires=[
        'pyyaml',
        'jsonschema',
        'requests',
        'pyhttp',
        'python-json-logger',
        'clint',
        'pyroute2'
    ],

    version=linuxiso.__version__,  # The version is write in linuxiso.__init__.py
    description='Download, custom and deploy (virtualbox) iso on linux',
    url='http://github.com/jcnaud/linuxiso',
    author='Jean-Charles Naud',
    author_email='jeancharles.naud@gmail.com',
    packages=[
        'linuxiso',
        'linuxiso.scripts',
        'linuxiso.custom',
        'linuxiso.ressources',
        'linuxiso.custom.receipts'],
    package_dir={'linuxiso': 'linuxiso'},
    include_package_data=True,
    package_data={'': ['*.json']},

    license='BSD',

    long_description=read('README.rst'),
    keywords='linux iso custom preseed debian ubuntu',  # Same keyword as github repo
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],

    entry_points={
        'console_scripts': [
            'downloadcli = linuxiso.scripts.downloadcli:main',
            'customcli = linuxiso.scripts.customcli:main',
            'virtualboxcli = linuxiso.scripts.virtualboxcli:main'
        ],
        #'gui_scripts': [
        #    'linuxisogui = xxxxx',
        #]
    }
)

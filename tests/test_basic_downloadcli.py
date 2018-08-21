#!/usr/bin/env python
# coding: utf-8

import os
import sys
import six
import subprocess
import json

# Local import
DIR_PWD = os.path.dirname(os.path.realpath(__file__))
PROGRAM = os.path.join(DIR_PWD, '..', 'scripts', 'downloadcli')


def run_cmd(cmd, raseit=False):
    """
    Run a command
    if error, print and raise it
    params cmd : String commande
    return out
    """
    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        process.check_returncode()
    except Exception as e:
        if raseit:
            print(
                str(e)
                + "\nCMD_SHELL : "+cmd
                + "\nSTDOUT : "+process.stdout.decode()
                + "\nSTDERR : "+process.stderr.decode(),
                exc_info=True)
        else:
            six.reraise(*sys.exc_info())

    return process.stdout.decode()


def test_help():
    """Test help option"""
    cmd = PROGRAM+' --help'
    result = run_cmd(cmd)

    # Compare result
    assert result


def test_list():
    """Test list option"""
    cmd = PROGRAM+' --list'
    result = run_cmd(cmd)

    # Compare result
    assert json.loads(result)

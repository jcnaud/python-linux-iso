#!/usr/bin/env python
# coding: utf-8

import os
import sys
import argparse
import logging
import json
import textwrap

# Local import
# DIR_PWD = os.path.dirname(os.path.realpath('__file__'))
# sys.path.append(os.path.join(DIR_PWD, ".."))
from linuxiso.download import Download  # noqa
from linuxiso.ressources.tools import load_conf  # noqa


def argument_parser():
    parser = argparse.ArgumentParser(
        prog='downloadcli',
        description='Program manage download of iso/image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            Example of standard usage:

                ./downloadcli --config ../examples/0_debian_simple/settings.yaml --list
                ./downloadcli --status debian-9.6.0-strech-amd64-netinst.iso
                ./downloadcli --download debian-9.6.0-strech-amd64-netinst.iso
            '''))

    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-f", "--config-file",
        help="load personnal configuration file (defaut: settings.yaml)",
        metavar="CONF_FILE")

    group.add_argument(
        "-l", "--list",
        help="list iso managed",
        action="store_true")
    group.add_argument(
        "-s", "--status",
        help="status of the iso/image",
        metavar="ISO_NAME")
    group.add_argument(
        "-S", "--status-all",
        help="status of all iso/image",
        action="store_true")
    group.add_argument(
        "-d", "--download",
        help="download the iso/image",
        metavar="ISO_NAME")
    group.add_argument(
        "-a", "--download-all",
        help="download all iso/image",
        action="store_true")
    group.add_argument(
        "-r", "--remove",
        help="remove the iso/image",
        metavar="ISO_NAME")
    group.add_argument(
        "-k", "--remove-all",
        help="remove all iso/image",
        action="store_true")

    group_vq = parser.add_mutually_exclusive_group()
    group_vq.add_argument(
        "-v", "-vv", "--verbose",
        help="enable verbosity: -v = INFO, -vv = DEBUG ",
        action="count",
        default=0)
    group_vq.add_argument(
        "-q", "--quiet",
        help="quiet mode",
        action="store_true")

    return parser


def main(args):
    """Parsing comnand line options/arguments"""

    if args:
        # Manage "verbose" and "quiet" options
        if args.verbose == 0:
            logging.basicConfig(level=logging.WARNING)
        elif args.verbose == 1:
            logging.basicConfig(level=logging.INFO)
        elif args.verbose >= 2:
            logging.basicConfig(level=logging.DEBUG)
        elif args.quiet:
            logging.basicConfig(level=logging.NOTSET)

        # Manage "config-file" options
        conf = load_conf(args.config_file)  # Manage None conf
        download = Download(conf=conf)

        # Manage options "list", "download", "download-all",
        #   "remove" and "remove-all"
        if args.list:             # List iso/image status
            result = download.list()
            print(json.dumps(result, indent=4, sort_keys=True))
        elif args.status:         # Get status of one iso
            result = download.status(args.status)
            print(json.dumps(result, indent=4, sort_keys=True))
        elif args.status_all:     # Get status of all iso
            result = download.status_all()
            print(json.dumps(result, indent=4, sort_keys=True))
        elif args.download:       # Download one iso/image
            download.download(args.download)
        elif args.download_all:   # Download all iso/image
            download.download_all()
        elif args.remove:         # Remove one iso/image
            download.remove(args.remove)
        elif args.remove_all:     # Remove all iso/image
            download.remove_all()
        else:
            parser.print_help()


if __name__ == "__main__":
    """Entry point for command ligne usage (with options/arguments)"""
    parser = argument_parser()
    args = parser.parse_args()
    main(args)

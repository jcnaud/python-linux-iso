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
from linuxiso.custom.core import Custom
from linuxiso.ressources.tools import load_conf


def argument_parser():
    parser = argparse.ArgumentParser(description='Program custom iso/image')

    epilog = textwrap.dedent('''\
        Example of standard usage:

            ./customcli --list
            ./customcli --status Custom-FullAuto-Debian-9-strech-amd64-\
netinst-server.iso
            ./customcli --create Custom-FullAuto-Debian-9-strech-amd64-\
netinst-server.iso
                --context context.yaml

        ''')

    parser = argparse.ArgumentParser(
        prog='Customcli',
        description='Program custom iso/image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog)

    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-f", "--config-file",
        help="load personnal configuration file (defaut: settings.yaml)",
        metavar="CONF_FILE")

    group.add_argument(
        "-l", "--list",
        help="list custom iso status",
        action="store_true")
    group.add_argument(
        "-s", "--status",
        help="status of the custom iso/image",
        metavar="ISO_NAME")
    group.add_argument(
        "-S", "--status-all",
        help="status of all custom iso/image",
        action="store_true")
    group.add_argument(
        "-r", "--remove",
        help="remove the custom iso/image",
        metavar="ISO_NAME")
    group.add_argument(
        "-k", "--remove-all",
        help="remove all custom iso/image",
        action="store_true")
    group.add_argument(
        "-c", "--create",
        help="create custom iso/image",
        metavar="ISO_NAME")

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
    """Parsing command line options/argument for custom module"""
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
        custom = Custom(conf=conf)

        # Manage "list", "status", ...
        if args.list:             # List custom iso/image status
            result = custom.list()
            print(json.dumps(result, indent=4, sort_keys=True))
        elif args.status:         # Get status of one custom iso
            result = custom.status(args.status)
            print(json.dumps(result, indent=4, sort_keys=True))
        elif args.status_all:     # Get status of all custom iso
            result = custom.status_all()
            print(json.dumps(result, indent=4, sort_keys=True))
        elif args.create:         # Create one custom iso/image
            custom.create(args.create)
        elif args.remove:         # Remove one customiso/image
            custom.remove(args.remove)
        elif args.remove_all:     # Remove all custom iso/image
            custom.remove_all()
        else:
            parser.print_help()


if __name__ == "__main__":
    """Entry point for command ligne usage (with options/arguments)"""
    parser = argument_parser()
    args = parser.parse_args()
    main(args)

# TODO: option s create and context
#
# class CreateAction(argparse.Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         if len(namespace.passwords) < len(namespace.users):
#             parser.error('Missing context')
#         else:
#             namespace.users.append(values)
#
#
# class ContextAction(argparse.Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         if len(namespace.users) <= len(namespace.passwords):
#             parser.error('Missing iso (create)')
#         else:
#             namespace.passwords.append(values)
#
#
# parser = argparse.ArgumentParser()
#
# parser.add_argument('--user', dest='users', default=[], action=UserAction, required=True)
#
# print(parser.parse_args())

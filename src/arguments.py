#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""
# ---------------------------------------------------------------------------
import argparse
from kankaclient.constants import (
    OUTPUT_OPTIONS,
    ENTITY_FORMAT
)
# ---------------------------------------------------------------------------


def get_parser():
    parser = argparse.ArgumentParser(
        prog='KankaManager', description='A simple command-line client for managing Kanka campaigns.', add_help=help
    )

    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='enable verbose logging')
    parser.add_argument('-c', '--config', action='store', default=None, help='path to Kanka config')

    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='command')

    parser_get = subparsers.add_parser('get', help='TODO')
    parser_get.add_argument('entity', action='store', type=str, help='TODO')
    parser_get.add_argument('-n', '--name', action='store', type=str, help='TODO')
    parser_get.add_argument('-f', '--field', action='store', type=str, default=[], dest='fields', nargs='*', help='TODO')
    parser_get.add_argument('--clean', action='store_true', default=False, help='TODO')
    parser_get.add_argument('-o', '--output', action='store', type=str, choices=OUTPUT_OPTIONS, help='TODO')

    parser_create = subparsers.add_parser('create', help='TODO')
    parser_create.add_argument('entity', action='store', type=str, help='TODO')
    parser_create.add_argument('-n', '--name', action='store', type=str, help='TODO')
    parser_create.add_argument('-f', '--file', action='store', type=str, help='TODO')
    parser_create.add_argument('-p', '--parameters', action='store', type=str, default=[], nargs='*', help='TODO')

    parser_update = subparsers.add_parser('update', help='TODO')
    parser_update.add_argument('entity', action='store', type=str, help='TODO')

    parser_delete = subparsers.add_parser('delete', help='TODO')
    parser_delete.add_argument('entity', action='store', type=str, help='TODO')
    parser_delete.add_argument('-n', '--name', action='store', dest='entities', type=str, nargs='+', help='TODO')

    parser_pull = subparsers.add_parser('pull', help='TODO')

    parser_push = subparsers.add_parser('push', help='TODO')

    parser_config = subparsers.add_parser('config', help='TODO')
    parser_config.add_argument('--file', help='TODO')
    parser_config.add_argument('--show', action='store_true', default=None, help='TODO')

    args = parser.parse_args()

    if hasattr(args, 'entity'):
        setattr(args, 'entity', ENTITY_FORMAT.get(args.entity, 'None'))
    if args.parameters:
        parameters = {}
        for _p in args.parameters:
            if '=' in _p:
                _p = _p.split('=')
                parameters[_p[0]] = _p[1]
        setattr(args, 'parameters', parameters)

    print()

    return args

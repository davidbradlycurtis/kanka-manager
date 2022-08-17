#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author: David Curtis
# Contact: davidbradlycurtis.com
# version ='1.0'
# ---------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""
# ---------------------------------------------------------------------------
import os
import logging
from arguments import get_parser
from cli.config import config, read_config
from cli.get import get
from utilities import get_logger
from kankaclient.constants import CONFIG
from kankaclient.client import KankaClient
# ---------------------------------------------------------------------------

LOGGER = get_logger()


def init(args):
    config_path = os.path.join(os.getcwd(), "kanka.conf")
    if args.config:
        config_path = os.path.normpath(args.config)

    return KankaClient(read_config(config_path))


commands = {
    "config": config,
    #TODO"create": create,
    #TODO"delete": delete,
    "get": get,
    #TODO"push": push,
    #TODO"pull": pull,
    #TODO"update": update,
}


def execute(args):
    if args.command == CONFIG:
        config(args)
    else:
        client = init(args)
        commands.get(args.command)(client, args)


def main():
    args = get_parser()
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    if args.command == CONFIG:
        config(args)
    else:
        client = init(args)
        commands.get(args.command)(client, args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""
# ---------------------------------------------------------------------------
from src.kankamanager.utilities import stamp


def get(client, args):
    if args.name is None:
        result = client.get_all(args.entity)
    else:
        result = [client.get(args.entity, args.name)]

    #TODO: Finish output format/process
    stamp(result, args)

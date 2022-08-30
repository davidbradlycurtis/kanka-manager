#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""
# ---------------------------------------------------------------------------
from utilities import get_logger

LOGGER = get_logger()

def delete(client, args):
    try:
        for entity in args.entities:
            if entity:
                client.delete(args.entity, entity)
    except Exception as ex:
        LOGGER.debug(ex)
        return False

    return True

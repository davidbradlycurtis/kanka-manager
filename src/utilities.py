#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
""" Contains program utility functions"""
# ---------------------------------------------------------------------------
import os
import json
import yaml
import logging
from prettytable import PrettyTable
from kankaclient.constants import (
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    DEFAULT_FIELDS
)
# ---------------------------------------------------------------------------

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
LOGGER = logging.getLogger("KankaManager")

class SpaceDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break('# ============================================================================================\n')


def get_logger():
    """ Initialize Logger """
    global LOGGER  # pylint: disable=global-statement
    if not LOGGER:
        log_formatter = logging.Formatter(
            fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT
        )
        handler = logging.StreamHandler()
        handler.setFormatter(log_formatter)
        LOGGER.addHandler(handler)

    return LOGGER

__all__ = [
    'get_logger'
]


def read_data(file):
    data = None
    if os.path.isfile(file):
        try:
            with open(file, 'r') as input_yaml:
                data = yaml.safe_load(input_yaml.read())
        except FileNotFoundError:
            pass
            #LOG ERROR
    return data


def stamp(entities, args):
    #TODO Finish
    if args.output == 'yaml':
        for entity in entities:
            yml = yaml.safe_dump(entity._asdict())
            print(yml)
    elif args.output == 'json':
        for entity in entities:
            js = json.dump(entity._asdict(), )
            print(js)
    elif args.output == 'table':
        columns = ['Name', 'ID', 'Type', 'Tags']
        if args.fields:
            columns.extend(args.fields)
        table = PrettyTable(columns)
        for entity in entities:
            row = [entity.name, entity.id, entity.type, entity.tags]
            for arg in args.fields:
                row.append(getattr(entity, arg))
            table.add_row(row)
        print(table)

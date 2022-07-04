import json
import os
import sys
import yaml
from kankaclient.constants import ENTITY_FORMAT

_format = {"yaml": yaml.safe_dump, "json": json.dump}

class SpaceDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break('# ============================================================================================\n')

def write_data(file, data):
    success = False
    if os.path.isfile(file):
        try:
            with open(file, 'w') as output_yaml:
                output_yaml.write(yaml.dump(data, Dumper=SpaceDumper, sort_keys=False))
            success = True
        except FileNotFoundError:
            pass
            #LOG ERROR
    return success

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


def is_plural(entity: str) -> bool:
    return entity.endswith(entity)


def etch(entities: list, args):
    if entities is None:
        # Log Error
        sys.exit(1)

    for entity in entities:
        if args.output == "yaml":
            output = _format.get(args.output)(entity)

        print(output)


def etch_all(entity_list, args):
    pass

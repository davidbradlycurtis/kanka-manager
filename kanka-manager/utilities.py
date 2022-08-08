import json
import os
import sys
import yaml
import logging
from kankaclient.constants import LOG_FORMAT, LOG_DATE_FORMAT, CONFIG_FIELDS

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
LOGGER = logging.getLogger("KankaManager")
_format = {"yaml": yaml.safe_dump, "json": json.dump}

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


def show_config(path):
    try:
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file)
            print('---Config---')
            print(f'Path: {path}')
            for field in config:
                print(f'-{field}: {config.get(field)}')
    except FileNotFoundError as ex:
        # Log error
        sys.exit(1)
    except yaml.YAMLError as ex:
        # Log error
        sys.exit(1)
    sys.exit(0)


def create_config(path):
    LOGGER.debug("Attempting to write to configuration file: %s", path)
    try:
        with open(path, "r+") as config_file:
            config = yaml.safe_load(config_file)
            print("---KankaManager Configuration---")
            for field in CONFIG_FIELDS:
                _input = input(CONFIG_FIELDS.get(field))
                config[field] = _input
            config_file.seek(0)
            config_file.truncate()
            yaml.safe_dump_all(config_file)
    except FileNotFoundError as ex:
        # Log error
        sys.exit(1)
    except yaml.YAMLError as ex:
        # Log error
        sys.exit(1)
    sys.exit(0)


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

import os
import sys
import yaml
import logging
from kankaclient.constants import LOG_FORMAT, LOG_DATE_FORMAT, CONFIG_FIELDS, CONFIG_FILE

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


def read_config(path: str) -> dict:
    config = dict()
    if path:
        try:
            with open(path, "r") as config_file:
                data = yaml.safe_load(config_file)
                config["campaign"] = data.get("campaign", None)
                config["campaign_dir"] = data.get("campaign_dir", None)
                config["token"] = data.get("token", None)
                config["throttle"] = data.get("throttle", True)
        except FileNotFoundError as ex:
            LOGGER.error('Failed to read config, file not found: %s', path)
            LOGGER.debug(ex)
            sys.exit(1)
        except yaml.YAMLError as ex:
            LOGGER.error("Unable to parse config file: %s", path)
            LOGGER.error("Problem: %s", ex.problem)
            LOGGER.error(ex.problem_mark)
            sys.exit(1)

    if None in config.values():
        LOGGER.error("Missing required config value. (campaign/campaign_dir/token)")
        sys.exit(1)

    return config


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
            print(config_file.read())
    except FileNotFoundError as ex:
        LOGGER.error('Failed to show config, file not found: %s', path)
        LOGGER.debug(ex)
        sys.exit(1)
    except yaml.YAMLError as ex:
        LOGGER.error('Failed to process config: %s', path)
        LOGGER.debug(ex)
        sys.exit(1)
    sys.exit(0)


def create_config(path):
    LOGGER.debug("Attempting to write to configuration file: %s", path)
    try:
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file)
            if config is None:
                config = dict()

            print("\n---KankaManager Configuration---")
            for field in CONFIG_FIELDS:
                _input = input(CONFIG_FIELDS.get(field))
                if _input:
                    config[field] = _input
                else:
                    if field not in config:
                        config[field] = None

        os.remove(path)
        with open(path, "w") as config_file:
            config_file.write(CONFIG_FILE.format(**config))

    except FileNotFoundError as ex:
        LOGGER.error('Failed to create config, file not found: %s', path)
        LOGGER.debug(ex)
        sys.exit(1)
    except yaml.YAMLError as ex:
        LOGGER.error('Failed to process config file: %s', path)
        LOGGER.debug(ex)
        sys.exit(1)

    print(f'Configuration file written to: {path}')
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

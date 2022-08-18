#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for"""
# ---------------------------------------------------------------------------
import os
import sys
import yaml
from utilities import (
    get_logger
)
from kankaclient.constants import CONFIG_FIELDS, CONFIG_FILE

LOGGER = get_logger()

def config(args):
    config_path = os.path.join(os.getcwd(), 'kanka.conf')
    if args.file:
        config_path = os.path.normpath(args.file)

    if not os.path.isfile(config_path):
        LOGGER.debug("Configuration file not found, creating a new file")
        open(config_path, "w")

    if args.show:
        show_config(config_path)
    else:
        create_config(config_path)

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

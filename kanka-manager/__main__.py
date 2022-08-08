import os
import logging
import sys
import yaml

from arguments import get_parser
from utilities import clogger, create_config, show_config
from kankaclient.constants import CONFIG_FIELDS, CONFIG, DEFAULT_CONFIG
from kankaclient.client import KankaClient

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
LOGGER = clogger.get_logger()
LOGGER = logging.getLogger("KankaManager")


def config(args):
    config_path = os.path.join(os.getcwd(), 'kanka.conf')
    if args.file:
        config_path = os.path.normpath(args.file)

    if not os.path.isfile(config_path):
        LOGGER.debug("Configuration file not found, creating a new file")
        with open(config_path, "w") as config_file:
            config_file.write(DEFAULT_CONFIG)

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
        except FileNotFoundError:
            LOGGER.error("File not found: %s", path)
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


def init(args):
    config_path = os.path.join(os.getcwd(), "kanka.conf")
    if args.config:
        config_path = args.config

    return KankaClient(read_config(config_path))


def create(args):
    pass


def delete(args):
    pass


def push(args):
    pass


def pull(args):
    pass


def update(args):
    pass


def get(args):
    client = init(args)
    if args.name is None:
        result = client.get_all(args.entity)
    result = client.get(args.entity, args.name)

    #TODO: Finish output format/process
    print(result)


commands = {
    "config": config,
    "create": create,
    "delete": delete,
    "get": get,
    "push": push,
    "pull": pull,
    "update": update,
}


def execute(args):
    if args.command == CONFIG:
        config(args)
    else:
        commands.get(args.command)(args)


def main():
    args = get_parser()
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    execute(args)


if __name__ == "__main__":
    main()

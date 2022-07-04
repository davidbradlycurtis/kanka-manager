import os
import logging
import sys
import yaml

from arguments import get_parser
from utilities import is_plural, etch, etch_all
from kankaclient.constants import CONFIG_FIELDS, CONFIG
from kankaclient.client import KankaClient

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
LOGGER = logging.getLogger("KankaManager")


def config(args):
    config_path = os.getcwd()
    if args.file:
        config_path = os.path.normpath(args.file)

    if not os.path.isfile(config_path):
        LOGGER.debug("Configuration file not found, creating a new file")
        open(config_path, "w")

    LOGGER.debug("Attempting to write to configuration file: %s", config_path)
    try:
        with open(config_path, "r") as config_file:
            config = yaml.safe_load_all(config_file)
            print("KankaManager Configuration")
            print()
            for field in CONFIG_FIELDS:
                print("Setting %s:", field)
                print(CONFIG_FIELDS.get(field))
                _input = input("->")
    except Exception:
        pass


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
    config_path = os.path.join(os.getcwd(), "kanka-manager", "kanka.yaml")
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
    if is_plural(args.entity) and args.name is None:
        etch_all(client.get_all(args.entity), args)
    entity = client.get(args.entity, args.name, args.clean)
    etch_entity(client.get(args.entity, args.name, args.clean), args)


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

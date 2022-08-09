import os
import logging

from arguments import get_parser
from utilities import get_logger, create_config, show_config, read_config
from kankaclient.constants import CONFIG
from kankaclient.client import KankaClient

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

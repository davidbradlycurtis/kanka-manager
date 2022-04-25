import argparse
from config import OUTPUT_OPTIONS


def get_parser():
    parser = argparse.ArgumentParser(
        prog='KankaManager', description='A simple command-line client for managing Kanka campaigns.', add_help=help
    )

    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='enable verbose logging')
    parser.add_argument('--config', action='store', default=None, help='path to Kanka config')

    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='command')

    parser_get = subparsers.add_parser('get', help='TODO')
    parser_get.add_argument('entity', action='store', type=str, help='TODO')
    parser_get.add_argument('-o', '--output', action='store', type=str, choices=OUTPUT_OPTIONS, help='TODO')

    parser_create = subparsers.add_parser('create', help='TODO')
    parser_create.add_argument('entity', action='store', type=str, help='TODO')

    parser_update = subparsers.add_parser('update', help='TODO')
    parser_update.add_argument('entity', action='store', type=str, help='TODO')

    parser_delete = subparsers.add_parser('delete', help='TODO')
    parser_delete.add_argument('entity', action='store', type=str, help='TODO')

    parser_pull = subparsers.add_parser('pull', help='TODO')

    parser_push = subparsers.add_parser('push', help='TODO')

    return parser.parse_args()

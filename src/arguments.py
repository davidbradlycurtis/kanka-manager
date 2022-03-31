import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        prog='KankaManager', description='A simple command-line client for managing Kanka campaigns.'
    )

    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='enable verbose logging')
    parser.add_argument('--config', action='store', default=None, help='path to Kanka config')
    
    subparsers = parser.add_subparsers()
    # create the parser for the "get" command
    parser_get = subparsers.add_parser('get', help='get help')
    parser_get.add_argument('entity', action='store_true')

    return parser.parse_args()
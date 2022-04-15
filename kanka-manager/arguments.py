import argparse
from config import COMMANDS

def base_parser():
    parser = argparse.ArgumentParser(
        prog='KankaManager', description='A simple command-line client for managing Kanka campaigns.'
    )

    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='enable verbose logging')
    parser.add_argument('--config', action='store', default=None, help='path to Kanka config')
    parser.add_argument('command', action='store', type=str, choices=COMMANDS, help='command to execute')


    return parser

def get(parser):
    parser.add_argument('entity', action='store', type=str, dest='entity', help='entity to get')

def get_parser():
    parser = base_parser()
    args = parser.parse_known_args()
    parser = get()
    

    return parser.parse_args()
from arguments import get_parser
from kankaclient.kankaclient import KankaClient

def main():
    args = get_parser()
    client = KankaClient()


if __name__ == '__main__':
    main()
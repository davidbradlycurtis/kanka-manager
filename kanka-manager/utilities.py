import json
import sys
import yaml
from kankaclient.constants import ENTITY_FORMAT

_format = {"yaml": yaml.safe_dump, "json": json.dump}


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

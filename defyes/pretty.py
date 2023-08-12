import json
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2, width=180, compact=True, underscore_numbers=True)

buildin_print = print
print = pp.pprint


def jprint(obj):
    """
    JSON style pretty printer.
    """
    buildin_print(json.dumps(obj, indent=2, default=lambda o: str(o)))

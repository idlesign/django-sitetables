import json
from typing import List, Tuple, Any


class JsEncoder(json.JSONEncoder):
    """Used by dump_js, applies special markup to callables to make them js functions."""

    def default(self, obj):

        if callable(obj):
            return '<--%s-->' % obj()

        return super().default(obj)


def dump_js(obj: dict) -> str:
    """Dumps dictionary to JS object."""

    return json.dumps(obj, cls=JsEncoder).replace('"<--', '').replace('-->"', '')


def contribute_to_dict(tuples: List[Tuple[str, Any]], to: dict):
    """Updates target dict using data from tuples.

    :param tuples: List of (key, value) tuples.
    :param to: Target dict.

    """
    for name, value in tuples:
        if value is not None:
            to[name] = value

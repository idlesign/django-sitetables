import json


class JsEncoder(json.JSONEncoder):
    """Used by dump_js, applies special markup to callables to make them js functions."""

    def default(self, obj):

        if callable(obj):
            return '<--%s-->' % obj()

        return super().default(obj)


def dump_js(obj: dict) -> str:
    """Dumps dictionary to JS object."""

    return json.dumps(obj, cls=JsEncoder).replace('"<--', '').replace('-->"', '')


def contribute_to_dict(items: dict, to: dict):
    """Updates target dict using data from tuples.

    :param items: List of (key, value) tuples.
    :param to: Target dict.

    """
    to.update({
        name: value
        for name, value in items.items()
        if value is not None
    })

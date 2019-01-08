import json


class JsEncoder(json.JSONEncoder):
    """Used by dump_js, applies special markup to callables to make them js functions."""

    def default(self, obj):

        if callable(obj):
            return '<--%s-->' % obj()

        return super().default(obj)


def dump_js(obj):
    """Dumps dictionary to JS object.

    :param dict obj:
    :rtype: str
    """
    return json.dumps(obj, cls=JsEncoder).replace('"<--', '').replace('-->"', '')


def contribute_to_dict(tuples, to):
    """Updates target dict using data from tuples.

    :param list[tuple] tuples: List of (key, value) tuples.
    :param dict to: Target dict.

    """
    for name, value in tuples:
        if value is not None:
            to[name] = value

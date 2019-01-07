
def contribute_to_dict(tuples, to):
    """Updates target dict using data from tuples.

    :param list[tuple] tuples: List of (key, value) tuples.
    :param dict to: Target dict.

    """
    for name, value in tuples:
        if value is not None:
            to[name] = value

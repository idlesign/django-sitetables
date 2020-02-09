from django.http import HttpRequest

from .toolbox.tables import Table


def respond(request: HttpRequest):
    """Responds to a serverside sitetable request.

    :param request:

    """
    return Table.respond(request)

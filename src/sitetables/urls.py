from django.urls import include, path

from . import views

urlpatterns = [
    path('responder/', views.respond, name='respond'),
]


def get_urlpatterns(urlbase: str = 'sitetables'):
    """Returns urlpatterns for sitetables
    that can be included into project's `urlpatterns`.

    :param urlbase: Base URL part to attach sitetables URLs under.

    """
    return path(f'{urlbase}/', include((urlpatterns, 'sitetables'), namespace='sitetables'))

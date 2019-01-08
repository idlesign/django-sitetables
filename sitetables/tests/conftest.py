from collections import OrderedDict

import pytest

from pytest_djangoapp import configure_djangoapp_plugin


pytest_plugins = configure_djangoapp_plugin()


@pytest.fixture()
def source_listdics():
    out = [
        OrderedDict([
            ('one', 'a'),
            ('two', 'b'),
            ('three', 'c'),
        ]),
        OrderedDict([
            ('one', 'd'),
            ('two', 'e'),
            ('three', 'f'),
        ]),
    ]
    return out


@pytest.fixture()
def setup_articles():
    from sitetables.tests.testapp.models import Article

    def setup_(count=5):

        for idx in range(count):
            article = Article(title='my %s' % idx)
            article.save()

    return setup_

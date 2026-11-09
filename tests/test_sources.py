import pytest

from sitetables.exceptions import SiteTablesException
from sitetables.tests.testapp.models import Article
from sitetables.toolbox import Table


def test_unsupported_source():

    with pytest.raises(SiteTablesException):
        Table('unsupported')


def test_source_deferred(source_listdics):

    table = Table()
    table.set_source(source_listdics)

    assert isinstance(table.get_rows(), list)


def test_source_listdicts(source_listdics):

    table = Table(
        source=source_listdics
    )
    rows = table.get_rows()

    assert len(rows) == 2
    assert rows[0]['one'] == 'a'
    assert rows[1]['two'] == 'e'
    assert table.source.row_id == 'one'


def test_source_model(setup_articles):

    source = Article

    table = Table(source)
    assert not table.get_rows()  # No articles in DB.

    setup_articles()

    table = Table(source)
    rows = list(table.get_rows())

    assert len(rows) == 5
    assert table.source.row_id == 'id'


def test_source_query_set(setup_articles):

    source = Article.objects.filter(hidden=False)

    assert not Table(source).get_rows()  # No articles in DB.

    setup_articles()

    assert len(Table(source).get_rows()) == 5

    article = Article(title='hidden')
    article.save()

    assert len(Table(source).get_rows()) == 6

    article.hidden = True
    article.save()

    table = Table(source)
    assert len(table.get_rows()) == 5  # Still 5 due to filtering
    assert table.source.row_id == 'id'

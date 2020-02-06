import pytest
from django.template import TemplateSyntaxError

from sitetables.plugins.style.bootstrap4 import Bootstrap4Plugin
from sitetables.toolbox import Table


@pytest.fixture()
def render(template_render_tag, template_context):

    def render_(table, tag):
        return template_render_tag('sitetables', tag + ' table', context=template_context({'table': table}))

    return render_


def test_assets(template_render_tag, template_context, source_listdics):

    table1 = Table(
        source=source_listdics,
        plugins=[Bootstrap4Plugin()]
    )

    table2 = Table(
        source=source_listdics,
        plugins=[Bootstrap4Plugin()]
    )

    context = template_context({'table1': table1, 'table2': table2})

    rendered_js = template_render_tag('sitetables', 'sitetables_js table1 table2', context=context)

    assert 'jquery.dataTables' in rendered_js
    assert 'bootstrap4' in rendered_js
    assert str(rendered_js).count('script') == 4

    rendered_css = template_render_tag('sitetables', 'sitetables_css table1 table2', context=context)

    assert 'jquery.dataTables' in rendered_css
    assert 'bootstrap4' in rendered_css
    assert str(rendered_css).count('link') == 2


def test_head(render, source_listdics):

    assert render(Table(source_listdics), tag='sitetable_head') == ''  # Because of no DOM init option.

    rendered = render(Table(
        source={
            'source': source_listdics,
            'options': {'init_dom': True},
        }
    ), tag='sitetable_head')

    assert '<th>one</th>' in rendered


def test_rows(render, source_listdics):

    assert render(Table(source_listdics), tag='sitetable_rows') == ''  # Because of no DOM init option.

    rendered = render(Table(
        source={
            'source': source_listdics,
            'options': {'init_dom': True},
        }
    ), tag='sitetable_rows')

    assert '<td>a</td>' in rendered


def test_sitetable_tag(template_render_tag, source_listdics):

    with pytest.raises(TemplateSyntaxError):
        template_render_tag('sitetables', 'sitetable_config table')

    Table(source_listdics, name='mytable')
    template_render_tag('sitetables', 'sitetable_config table', context={'table': 'mytable'})


def test_config(render, source_listdics):

    rendered = render(Table(source_listdics), tag='sitetable_config')

    assert '"columns":' in rendered
    assert '"data":' in rendered
    assert '"name": "one"' in rendered
    assert '"one": "a"' in rendered
    assert "function" in rendered
    assert '"function' not in rendered

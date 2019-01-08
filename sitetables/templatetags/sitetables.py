from django import template
from django.template import TemplateSyntaxError
from django.utils.safestring import SafeText

from ..toolbox.utils import dump_js

if False:  # pragma: nocover
    from ..toolbox import Table


register = template.Library()


def get_asset(attrname, tables):
    assets = {}

    for table in tables:  # type: Table
        for asset in getattr(table, attrname)():
            assets[asset] = ''  # Making a unique list.

    return SafeText(' '.join(assets.keys()))


def sitetable_tag(func):

    func_name = func.__name__

    def sitetable_tag_(table):

        if isinstance(table, str):
            raise TemplateSyntaxError(
                '`%s` template tag expects sitetable object. `%s` is given instead' % (func_name, type(table)))

        return SafeText(func(table))

    return register.simple_tag(sitetable_tag_, name=func_name)


@register.simple_tag()
def sitetables_js(*args):
    """

    :param list[Table] args:
    :rtype: str
    """
    return get_asset('get_assets_js', args)


@register.simple_tag()
def sitetables_css(*args):
    """

    :param list[Table] args:
    :rtype: str
    """
    return get_asset('get_assets_css', args)


@sitetable_tag
def sitetable_config(table):
    """

    :param Table table:
    :rtype: str
    """
    return dump_js(table.get_config())


@sitetable_tag
def sitetable_head(table):
    """

    :param Table table:
    :rtype: str
    """
    if not table.source.options.get('init_dom'):
        return ''

    return '<tr><th>%s</th></tr>' % '</th><th>'.join('%s' % column.title for column in table.get_columns().values())


@sitetable_tag
def sitetable_rows(table):
    """

    :param Table table:
    :rtype: str
    """
    if not table.source.options.get('init_dom'):
        return ''

    cols = list(table.get_columns().keys())
    return ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % row[col] for col in cols) for row in table.get_rows())

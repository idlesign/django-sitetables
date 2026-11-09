from typing import Tuple, Union

from django import template
from django.template import TemplateSyntaxError
from django.utils.safestring import SafeText

from ..toolbox.utils import dump_js
from ..toolbox import Table


register = template.Library()

TypeTableDef = Union[Table, str]


def resolve_table(table_def: TypeTableDef):

    if isinstance(table_def, str):
        try:
            return Table.tables_registry[table_def]

        except KeyError:
            raise TemplateSyntaxError(
                f'Sitetable with alias `{table_def}` is not found. '
                f"Registered tables: {','.join(Table.tables_registry.keys())}.")

    return table_def


def get_asset(attrname: str, tables: Tuple[TypeTableDef, ...]):

    assets = {}

    for table in tables:

        if not table:
            continue

        table = resolve_table(table)
        func_get_asset = getattr(table, attrname, None)

        if func_get_asset is None:
            raise ValueError(f"Template variable {table} doesn't seem to represent a sitetable.")

        for asset in func_get_asset():
            assets[asset] = ''  # Making a unique list.

    return SafeText(' '.join(assets.keys()))


def sitetable_tag(func):

    func_name = func.__name__

    def sitetable_tag_(table: TypeTableDef):
        table = resolve_table(table)
        return SafeText(func(table))

    return register.simple_tag(sitetable_tag_, name=func_name)


@register.simple_tag()
def sitetables_js(*args: TypeTableDef) -> str:
    return get_asset('get_assets_js', args)


@register.simple_tag()
def sitetables_css(*args: TypeTableDef) -> str:
    return get_asset('get_assets_css', args)


@sitetable_tag
def sitetable_config(table: Table) -> str:
    return dump_js(table.get_config())


@sitetable_tag
def sitetable_head(table: Table) -> str:
    if not table.source.options.get('init_dom'):
        return ''

    cells = '</th><th>'.join(
        f'{column.title}'
        for column in table.get_columns().values()
    )
    return f'<tr><th>{cells}</th></tr>'


@sitetable_tag
def sitetable_rows(table: Table) -> str:
    if not table.source.options.get('init_dom'):
        return ''

    cols = list(table.get_columns().keys())

    return ''.join('<tr>%s</tr>' % ''.join(
        f'<td>{row[col]}</td>' for col in cols
    ) for row in table.get_rows())

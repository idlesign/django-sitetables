from itertools import chain
from typing import Optional, List, Union, Dict

from django.db.models import QuerySet, Model

from .columns import TableColumn

if False:  # pragma: nocover
    from .tables import Table


TypeTableSource = Union[Dict, List[Dict], Model, QuerySet]


class TableSource:
    """Base data source for tables."""

    def __init__(self, source, options: Optional[dict] = None):
        self.columns = {}
        self.row_id = 'DT_RowId'
        self.options = options or {}
        self._rows = []
        self._bootstrap(source)

    @classmethod
    def spawn(cls, source, params: dict) -> 'TableSource':
        """Alternative constructor.

        :param source:
        :param params:

        """
        source_obj = cls(source, options=params.get('options'))
        return source_obj

    def _bootstrap(self, source: TypeTableSource):
        """The place for a source-specific bootstrap."""

    def contribute_to_config(self, config: dict, table: 'Table'):
        """Updates table configuration dictionary with source-specific params.

        :param config:
        :param table:

        """
        config.update({
            'createdRow': lambda: (
                "function(row, data, idx){var v=data['%s']; if (v){$(row).attr('data-id', v);}}" % self.row_id),

            'processing': True,
            'columns': [column.as_dict() for column in self.columns.values()],
        })

        options = self.options

        if not options.get('init_dom'):
            # todo maybe use serialization instead of string casting
            # todo FK support
            config['data'] = [{k: f'{v}' for k, v in row.items()} for row in self.rows]

    @property
    def rows(self) -> List[dict]:
        """Represents table rows."""

        return self._rows


class ListDictsSource(TableSource):
    """Static data source.

    .. code-block:: python

        source = [
            {
                'one': '1',
                'two': '2',
            },
            {
                'one': '3',
                'two': '4',
            },
        ]

    """
    def _bootstrap(self, source: List[dict]):
        super()._bootstrap(source)

        columns = self.columns

        names = list(source[0].keys())

        for name in names:
            columns[name] = TableColumn(name=name)

        self._rows = source
        self.row_id = names[0]  # Use first column value.


class ModelSource(TableSource):
    """Django model datasource.

    .. code-block:: python

        source = Article  # Model class.
        source = Article.objects.filter(hidden=False)  # Or a QuerySet.

    """
    def _bootstrap(self, source: Union[Model, QuerySet]):
        super()._bootstrap(source)

        columns = self.columns

        if isinstance(source, QuerySet):
            model = source.model
            qs = source

        else:
            # Model class
            model = source
            qs = model.objects.all()

        opts = model._meta

        for field in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            name = field.name
            columns[name] = TableColumn(name=name, title=field.verbose_name, source=field)

        self.model = model
        self.qs = qs

        self.row_id = opts.pk.name

    @property
    def rows(self) -> List[dict]:
        columns = self.columns
        result = self.qs.values(*columns.keys())
        return result

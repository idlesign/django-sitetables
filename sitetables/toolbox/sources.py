from collections import OrderedDict
from itertools import chain

from django.db.models import QuerySet

from .columns import TableColumn


class TableSource:
    """Base data source for tables."""

    def __init__(self, source, options=None):
        self.columns = OrderedDict()
        self.row_id = 'DT_RowId'  # todo may clash among tables of one page
        self.options = options or {}
        self._rows = []
        self._bootstrap(source)

    @classmethod
    def spawn(cls, source, params):
        """Alternative constructor.

        :param source:
        :param dict params:
        :rtype: TableSource

        """
        source_obj = cls(source, options=params.get('options'))
        return source_obj

    def _bootstrap(self, source):
        """The place for a source-specific bootstrap."""

    def contribute_to_config(self, config, table):
        """Updates table configuration dictionary with source-specific params.

        :param dict config:
        :param Table table:

        """
        config.update({
            'rowId': self.row_id,
            'processing': True,
            'columns': [column.as_dict() for column in self.columns.values()],
        })

        options = self.options

        if not options.get('init_dom'):
            # todo maybe use serialization instead of string casting
            # todo FK support
            config['data'] = [{k: '%s' % v for k, v in row.items()} for row in self.rows]

    @property
    def rows(self):
        """Represents table rows.

        :rtype: list[dict]
        """
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

    def _bootstrap(self, source):
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

    def _bootstrap(self, source):
        super()._bootstrap(source)

        columns = self.columns

        if isinstance(source, QuerySet):
            model = source.model
            qs = source

        else:  # Model class
            model = source
            qs = model.objects.all()

        opts = model._meta

        for field in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            name = field.name
            columns[name] = TableColumn(name=name, title=field.verbose_name, source=field)

        self.model = model
        self.qs = qs

        self.row_id = 'pk'

    @property
    def rows(self):
        columns = self.columns
        result = self.qs.values(*columns.keys())
        return result

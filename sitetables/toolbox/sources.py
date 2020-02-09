import re
from collections import namedtuple
from itertools import chain
from typing import Optional, List, Union, Dict, Type, Tuple

from django.db.models import QuerySet, Model
from django.http import HttpRequest, JsonResponse
from django.urls import reverse

from .columns import TableColumn

if False:  # pragma: nocover
    from .tables import Table


TypeTableSource = Union[Dict, List[Dict], Type[Model], QuerySet]
TypeTableColumns = Dict[str, TableColumn]
TypeFilteredItems = Union[QuerySet, List]
TypeServerItems = Tuple[int, int, TypeFilteredItems]
TypePreparedItems = List[Dict[str, str]]

TableItemsFilter = namedtuple('TableItemsFilter', [
    'start',
    'length',
    'search',
    'order',
])


class TableSource:
    """Base data source for tables."""

    columns: TypeTableColumns
    _columns_by_idx: Dict[int, TableColumn]

    _url_responder = None
    _RE_COLUMN_DEF = re.compile(r'\[(\d+)\]\[([a-z]+)\]')

    def __init__(self, source, options: Optional[dict] = None):
        self.columns = {}
        self._columns_by_idx = {}
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
        return cls(source, options=params.get('options'))

    def _server_get_filter(self, source: dict) -> TableItemsFilter:
        """Returns a filter object composed from source dictionary
        (e.g. POST params).

        :param source:

        """
        by_idx = self._columns_by_idx
        re_def = self._RE_COLUMN_DEF

        order = []

        length_default = 10

        length = int(source.get('length', length_default))
        if length > 5000:
            length = length_default

        start = int(source.get('start', 0))

        items_filter = TableItemsFilter(
            start=start,
            length=length,
            search=source.get('search[value]', '').strip() or '',
            order=order,
        )

        source = dict(sorted(source.items(), key=lambda item: item[0]))

        for key, val in source.items():

            if key.startswith('order'):

                match = re_def.search(key)

                if not match:
                    continue

                if match.group(2) == 'dir':
                    continue

                column_idx = int(val)
                column_name = by_idx.get(column_idx)

                if not column_name:
                    continue

                order_desc = source.get(f'order[{match.group(1)}][dir]', 'asc') == 'desc'
                order.append(f"{'-' if order_desc else ''}{column_name}")

        return items_filter

    def _server_get_items(self, items_filter: TableItemsFilter = None) -> TypeServerItems:
        """Must return serverside items filtered using th given filter.

        :param items_filter:

        """
        raise NotImplementedError  # pragma: nocover

    def _server_prepare_items(self, items: TypeFilteredItems) -> TypePreparedItems:
        """Prepares items for on_server response.

        :param items:

        """
        return items

    def respond(self, request: HttpRequest) -> JsonResponse:
        """

        https://datatables.net/manual/server-side

        :param request:

        """
        source = request.POST

        items_filter = self._server_get_filter(source.dict())

        count_total, count_filtered, filtered = self._server_get_items(items_filter)

        start = items_filter.start
        filtered = filtered[start:start+items_filter.length]

        filtered = self._server_prepare_items(filtered)

        draw = source.get('draw', 1)
        draw = int(draw)  # As per docs.

        out = {
            'data': filtered,
            'draw': draw,
            'recordsTotal': count_total,
            'recordsFiltered': count_filtered,
        }

        return JsonResponse(out)

    def _get_columns(self) -> TypeTableColumns:
        """Should return columns dictionary."""
        columns = {}

        for name, title in self.options.get('columns_add', {}).items():
            columns[name] = TableColumn(name=name, title=title)

        return columns

    def _bootstrap(self, source: TypeTableSource):
        """The place for a source-specific bootstrap."""
        columns = self._get_columns()
        self.columns = columns
        self._columns_by_idx = {idx: column for idx, column in enumerate(columns)}

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

        if options.get('on_server', False):

            url_responder = self._url_responder

            if url_responder is None:
                url_responder = self.__class__._url_responder = reverse('sitetables:respond')

            config.update({
                'serverSide': True,
                'ajax': {
                    'url': url_responder,
                    'type': 'POST',
                    'data': {
                        'tableName': table.name,
                    }
                },
            })

        else:

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
    def _bootstrap(self, source: TypeTableSource):

        names = list(source[0].keys())
        self.options['columns_add'] = dict.fromkeys(names, '')

        self._rows = source
        self.row_id = names[0]  # Use first column value.

        super()._bootstrap(source)


class ModelSource(TableSource):
    """Django model datasource.

    .. code-block:: python

        source = Article  # Model class.
        source = Article.objects.filter(hidden=False)  # Or a QuerySet.

    """
    model: Type[Model] = None

    def _get_columns(self) -> TypeTableColumns:
        columns = {}

        meta = self.model._meta

        for field in chain(meta.concrete_fields, meta.private_fields, meta.many_to_many):
            name = field.name
            columns[name] = TableColumn(name=name, title=field.verbose_name, source=field)

        columns.update(super()._get_columns())

        return columns

    def _bootstrap(self, source: TypeTableSource):

        if isinstance(source, QuerySet):
            model = source.model
            qs = source

        else:
            # Model class
            model = source
            qs = model.objects.all()

        self.model = model
        self.qs = qs
        self.row_id = model._meta.pk.name

        super()._bootstrap(source)

    def _server_get_items(self, items_filter: TableItemsFilter = None) -> TypeServerItems:

        qs = self.qs

        filter_kwargs = {}

        search = items_filter.search

        if search:
            filter_kwargs['title__contains'] = search

        objects = qs.filter(**filter_kwargs)

        count_total = qs.count()
        count_filtered = objects.count()

        order = items_filter.order

        if order:
            objects = objects.order_by(*order)

        return count_total, count_filtered, objects

    def _server_prepare_items(self, items: TypeFilteredItems) -> TypePreparedItems:

        dicts = []

        columns = self.columns

        for model in items:

            item_data = {}

            for column_name, column in columns.items():

                if column.source is None:
                    # Model property.
                    item_data[column_name] = getattr(model, column_name)

                else:
                    # Model field.
                    item_data[column_name] = column.source.value_from_object(model)

            dicts.append(item_data)

        return dicts

    @property
    def rows(self) -> List[dict]:
        columns = self.columns
        _, _, qs = self._server_get_items(TableItemsFilter(
            start=0,
            length=0,
            search='',
            order=[],
        ))
        result = qs.values(*columns.keys())
        return result

from gettext import gettext
from typing import List, Optional, Dict
from uuid import uuid4
from weakref import WeakValueDictionary

from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse

from .sources import ModelSource, ListDictsSource, TypeTableSource
from ..exceptions import SiteTablesException
from ..settings import URL_CDN_BASE

if False:  # pragma: nocover
    from ..plugins.base import TablePlugin


class Table:
    """Represents a sitetable."""

    version = '1.10.20'

    assets = {
        'js': [
            'jquery.dataTables.min.js',
        ],
        'css': [
            'jquery.dataTables.min.css',
        ],
    }

    tables_registry: Dict[str, 'Table'] = WeakValueDictionary()
    """Known table instances."""

    __tables_kept = []

    def __init__(
            self,
            source: Optional[TypeTableSource] = None,
            *,
            plugins: Optional[List['TablePlugin']] = None,
            on_server: bool = False,
            name: str = None
    ):
        """
        :param source: Table data source.

        :param plugins: A list of plugins.

        :param on_server: Do not pour all table data to a client at once,
            but issue requests to a server to get data.

        :param name: Table name (alias) to differentiate among
            different tables. If not set, default will be used.

        """
        self.source = None
        self.on_server = on_server
        self.set_source(source)
        self.plugins = plugins or []
        self.url_base = URL_CDN_BASE

        cls = self.__class__

        if name:
            # Keep named tables alive in weakrefdict.
            cls.__tables_kept.append(self)

        else:
            name = f'table-{uuid4()}'

        self.name = name

        cls.tables_registry[name] = self

        # todo options argument maybe as a class?

    def set_source(self, source: TypeTableSource):
        """Sets a data source for this table.

        :param source: Table data source.

        """
        if source is None:
            return None

        params = {}

        if isinstance(source, dict):
            params.update(source)
            source = source['source']

        options = params.setdefault('options', {})
        options['on_server'] = self.on_server

        if isinstance(source, list):
            source_cls = ListDictsSource

        elif isinstance(source, QuerySet) or (type(source) == type(Model)):
            source_cls = ModelSource

        else:
            raise SiteTablesException(f'Unsupported data source type: {type(source)}')

        self.source = source_cls.spawn(source, params)

    def get_config(self) -> dict:
        """Returns a table configuration dictionary including params from plugins."""

        source = self.source

        config = {}

        source.contribute_to_config(config, self)

        for plugin in self.plugins:
            plugin.contribute_to_config(config, table=self)

        return config

    def get_columns(self) -> dict:
        """Returns columns dictionary from data source."""

        return self.source.columns

    def get_rows(self) -> List[dict]:
        """Returns table rows from data source."""

        return self.source.rows

    @property
    def url_version(self) -> str:
        """Base URL for current DataTables version."""

        return self.url_base + self.version + '/'

    @property
    def url_plugins(self) -> str:
        """Base URL for plugins for current DataTables version."""

        return self.url_base + 'plug-ins/' + self.version + '/'

    def get_assets(self, typename: str, enclosure: str) -> List[str]:
        """Returns a list of assets inclusion directives with their URLs.

        :param typename: Assets type name. E.g.: js, css.
        :param enclosure: Pattern to place URL into.

        """
        # todo checksum origin support

        assets = []

        url_asset_base = self.url_version + typename + '/'

        def contribute_assets(src):
            for asset in src.assets.get(typename, []):
                assets.append(enclosure % {'url': url_asset_base + asset})

        contribute_assets(self)

        for plugin in self.plugins:
            contribute_assets(plugin)

        return assets

    def get_assets_js(self) -> List[str]:
        """Returns a list of HTML directives to include JS relevant for table and plugins."""

        return self.get_assets('js', '<script src="%(url)s"></script>')

    def get_assets_css(self) -> List[str]:
        """Returns a list of HTML directives to include CSS relevant for table and plugins."""

        return self.get_assets('css', '<link rel="stylesheet" href="%(url)s">')

    @classmethod
    def respond(cls, request: HttpRequest) -> JsonResponse:
        """Responds to a serverside sitetable request.

        :param request:

        """
        table_name = request.POST.get('tableName', '')
        table = Table.tables_registry.get(table_name)

        if not table:
            return JsonResponse({
                'error': gettext('No data found for "%(table)s" table') % {'table': table_name},
            }, status=400)

        return table.source.respond(request)

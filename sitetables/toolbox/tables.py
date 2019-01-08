from django.db.models import Model, QuerySet

from .sources import ModelSource, ListDictsSource
from ..exceptions import SiteTablesException
from ..settings import URL_CDN_BASE

if False:  # pragma: nocover
    from ..plugins.base import TablePlugin


class Table:
    """Represents a sitetable."""

    version = '1.10.19'

    assets = {
        'js': [
            'jquery.dataTables.min.js',
        ],
        'css': [
            'jquery.dataTables.min.css',
        ],
    }

    def __init__(self, source=None, plugins=None, name=None):
        """
        :param dict|list|Model|QuerySet source: Table data source.

        :param list[TablePlugin] plugins: A list of plugins.

        :param str name: Table name (alias) to differentiate among
            different tables. If not set, default will be used.

        """
        self.source = None
        self.set_source(source)
        self.plugins = plugins or []
        self.url_base = URL_CDN_BASE
        self.name = name or 'table'

        # todo options argument maybe as a class?

    def set_source(self, source):
        """Sets a data source for this table.

        :param dict|list|Model|QuerySet source: Table data source.

        """
        if source is None:
            return None

        params = {}
        if isinstance(source, dict):
            params = source
            source = source['source']

        if isinstance(source, list):
            source_cls = ListDictsSource

        elif isinstance(source, QuerySet) or (type(source) == type(Model)):
            source_cls = ModelSource

        else:
            raise SiteTablesException('Unsupported data source type: %s' % type(source))

        self.source = source_cls.spawn(source, params)

    def get_config(self):
        """Returns a table configuration dictionary including params from plugins.

        :rtype: dict
        """
        source = self.source

        config = {}

        source.contribute_to_config(config, self)

        for plugin in self.plugins:
            plugin.contribute_to_config(config, table=self)

        return config

    def get_columns(self):
        """Returns columns dictionary from data source.

        :rtype: OrderedDict
        """
        return self.source.columns

    def get_rows(self):
        """Returns table rows from data source.

        :rtype: list[dict]

        """
        return self.source.rows

    @property
    def url_version(self):
        """Base URL for current DataTables version.

        :rtype: str
        """
        return self.url_base + self.version + '/'

    @property
    def url_plugins(self):
        """Base URL for plugins for current DataTables version.

        :rtype: str
        """
        return self.url_base + 'plug-ins/' + self.version + '/'

    def get_assets(self, typename, enclosure):
        """Returns a list of assets inclusion directives with their URLs.

        :param str typename: Assets type name. E.g.: js, css.
        :param str enclosure: Pattern to place URL into.

        :rtype: list
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

    def get_assets_js(self):
        """Returns a list of HTML directives to include JS relevant for table and plugins.

        :rtype: list
        """
        return self.get_assets('js', '<script src="%(url)s"></script>')

    def get_assets_css(self):
        """Returns a list of HTML directives to include CSS relevant for table and plugins.

        :rtype: list
        """
        return self.get_assets('css', '<link rel="stylesheet" href="%(url)s">')

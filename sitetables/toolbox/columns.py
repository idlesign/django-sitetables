from .utils import contribute_to_dict


class TableColumn:
    """Represents a table column."""

    def __init__(self, name, title=None, source=None, sort=None, search=None, default=None, css=None):
        """
        :param str name: Column name (alias).
        :param str title: Column title.
        :param source: Column source object
        :param bool sort: Flag to toggle sorting.
        :param bool search: Flag to toggle searching.
        :param str default: Value to be used if no data available.
        :param str css: CSS class for the column.

        """
        self.name = name
        self.title = title or name
        self.source = source
        self.sort = sort
        self.search = search
        self.default = default
        self.css = css

        # todo decide on `render` js

    def as_dict(self):
        """Represents the column as a dictionary.

        :rtype: dict
        """
        name = self.name

        result = {
            'data': name,
            'name': name,
            'title': '%s' % self.title,
        }

        contribute_to_dict([
            ('sortable', self.sort),
            ('searchable', self.search),
            ('defaultContent', self.default),
            ('className', self.css),
        ], to=result)

        return result

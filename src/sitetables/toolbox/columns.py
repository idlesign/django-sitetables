from typing import Any

from .utils import contribute_to_dict


class TableColumn:
    """Represents a table column."""

    def __init__(
            self,
            name: str,
            title: str = None,
            source: Any = None,
            sort: bool = None,
            search: bool = None,
            default: str = None,
            css: str = None
    ):
        """
        :param name: Column name (alias).
        :param title: Column title.
        :param source: Column source object
        :param sort: Flag to toggle sorting.
        :param search: Flag to toggle searching.
        :param default: Value to be used if no data available.
        :param css: CSS class for the column.

        """
        self.name = name
        self.title = title or name
        self.source = source
        self.sort = sort
        self.search = search
        self.default = default
        self.css = css

        # todo decide on `render` js

    def as_dict(self) -> dict:
        """Represents the column as a dictionary."""

        name = self.name

        result = {
            'data': name,
            'name': name,
            'title': f'{self.title}',
        }

        contribute_to_dict({
            'sortable': self.sort,
            'searchable': self.search,
            'defaultContent': self.default,
            'className': self.css,
        }, to=result)

        return result

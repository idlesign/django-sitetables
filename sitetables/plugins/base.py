
if False:  # pragma: nocover
    from ..sitetable import Table


class TablePlugin:
    """Base class for plugins."""

    assets = {}
    """For additional plugin-related assets (js, css).

    Example:    
        assets = {
            'js': [
                'some.js',
            ],
            'css': [
                'some.css',
            ],
        }
    
    """

    def contribute_to_config(self, config, table):
        """Allows updating base table configuration dictionary with
        values from plugin specific.

        :param dict config:
        :param Table table:

        """

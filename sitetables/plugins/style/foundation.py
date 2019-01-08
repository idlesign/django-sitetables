from ..base import TablePlugin


class FoundationPlugin(TablePlugin):

    assets = {
        'js': [
            'dataTables.foundation.min.js',
        ],
        'css': [
            'dataTables.foundation.min.css',
        ],
    }

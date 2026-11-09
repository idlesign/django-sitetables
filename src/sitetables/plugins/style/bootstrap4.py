from ..base import TablePlugin


class Bootstrap4Plugin(TablePlugin):

    assets = {
        'js': [
            'dataTables.bootstrap4.min.js',
        ],
        'css': [
            'dataTables.bootstrap4.min.css',
        ],
    }

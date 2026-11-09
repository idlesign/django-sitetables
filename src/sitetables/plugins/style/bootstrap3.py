from ..base import TablePlugin


class Bootstrap3Plugin(TablePlugin):

    assets = {
        'js': [
            'dataTables.bootstrap.min.js',
        ],
        'css': [
            'dataTables.bootstrap.min.css',
        ],
    }

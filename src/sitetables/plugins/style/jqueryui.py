from ..base import TablePlugin


class JqueryUiPlugin(TablePlugin):

    assets = {
        'js': [
            'dataTables.jqueryui.min.js',
        ],
        'css': [
            'dataTables.jqueryui.min.css',
        ],
    }

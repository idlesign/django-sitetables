from ..base import TablePlugin


class SemanticPlugin(TablePlugin):

    assets = {
        'js': [
            'dataTables.semanticui.min.js',
        ],
        'css': [
            'dataTables.semanticui.min.css',
        ],
    }

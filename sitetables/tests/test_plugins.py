from django.utils.translation import activate, deactivate_all

from sitetables.plugins.i18n import I18nPlugin
from sitetables.plugins.style.bootstrap4 import Bootstrap4Plugin
from sitetables.toolbox import Table


def test_bootstrap4(source_listdics):

    table = Table(
        source=source_listdics,
        plugins=[
            Bootstrap4Plugin(),
        ]
    )

    assert len(table.get_assets_css()) == 2
    assert len(table.get_assets_js()) == 2


def test_i18n(source_listdics, settings):

    table = Table(source=source_listdics, plugins=[I18nPlugin()])

    assert len(table.get_assets_css()) == 1
    assert len(table.get_assets_js()) == 1

    config = table.get_config()
    assert 'language' not in config  # Unable to autodetect lang

    activate('ru')

    # Autodetect.
    config = table.get_config()
    assert 'Russian' in config['language']['url']

    # Manual.
    config = Table(source=source_listdics, plugins=[I18nPlugin('de')]).get_config()
    assert 'German' in config['language']['url']

    deactivate_all()

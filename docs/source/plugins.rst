Plugins
=======

Additional functionality and appearance for tables are available through plugins.

You can activate certain plugins using ``plugins`` argument for ``Table``.

.. code-block:: python

    from sitetables.plugins.i18n import I18nPlugin
    from sitetables.plugins.style.bootstrap4 import Bootstrap4Plugin
    from sitetables.toolbox import Table

    table_entries = Table(
        source=source
        plugins=[
            # Let's activate a couple of plugins.
            I18nPlugin(),
            Bootstrap4Plugin(),
        ],
    )


Include plugin assets (JS, CSS) on your pages using
``{% sitetables_css table_entries %}`` and ``{% sitetables_js table_entries %}`` template tags.


.. note::

    Find plugins in ``sitetables.plugins`` package.


Styling (themes)
----------------

Theme plugins are available in ``sitetables.plugins.style`` package.

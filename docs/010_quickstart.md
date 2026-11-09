Quickstart
==========


First place table definition into ``views.py``:

.. code-block:: python

    from django.shortcuts import render
    from sitetables.plugins.i18n import I18nPlugin
    from sitetables.plugins.style.bootstrap4 import Bootstrap4Plugin
    from sitetables.toolbox import Table

    from .models import Entries


    def entries(request):
        # We create client-side handled table from entries queryset,
        table_entries = Table(
            source=Entries.objects.filter(hidden=False),
            # We also activate some plugins.
            plugins=[
                I18nPlugin(),
                Bootstrap4Plugin(),
            ],
        )
        return render(request, 'entries.html', {'table_entries': table_entries})


Next create page template ``entries.html``:

.. code-block:: html

    {% load sitetables %}

    <!-- The following line usually goes into head tag. It'll load all needed css. -->
    {% sitetables_css table_entries %}

    <!-- The following resides in body tag. Note that in this scenario
         thead and tbody will be populated using JS automatically. -->
    <table id="table-entries" class="table table-striped table-condensed">
        <thead></thead><tbody></tbody>
    </table>

    <script type="text/javascript">
         $(function() {
             <!-- Initialize table using generated config.
                  The following demonstrates how you can extend generated
                  configuration. -->
             $('#table-entries').dataTable($.extend({},
                 {% sitetable_config table_entries %},
                 {
                     pagingType: 'full_numbers',
                     lengthChange: false,
                 }
             ));

         });
     </script>

    <!-- The following line usually goes somewhere near the end of the body.
         It'll load all needed js. -->
    {% sitetables_js table_entries %}


Serverside tables
~~~~~~~~~~~~~~~~~

You can instruct ``sitetables`` to not to pour all table data to client, but
to fetch it from server when needed. For that pass ``on_server=True`` to ``Table``:

.. code-block:: python

    table_entries = Table(source=Entries, on_server=True)


Addressing tables by name
~~~~~~~~~~~~~~~~~~~~~~~~~

One may not spawn a table for each request, but create named table and address it by its name:

.. code-block:: python

    ENTRIES_TABLE_NAME = 'entries'
    Table(source=Entries, name=ENTRIES_TABLE_NAME)

    def entries(request):
        return render(request, 'entries.html', {'table_entries': ENTRIES_TABLE_NAME})

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
        # We create table from entries queryset,
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
             <!-- Initialize table using generated config. -->
             $('#table-entries').dataTable({% sitetable_config table_entries %});
         });
     </script>

    <!-- The following line usually goes somewhere near the end of the body.
         It'll load all needed js. -->
    {% sitetables_js table_entries %}

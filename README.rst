django-sitetables
=================
https://github.com/idlesign/django-sitetables

|release| |lic| |ci| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/django-sitetables.svg
    :target: https://pypi.python.org/pypi/django-sitetables

.. |lic| image:: https://img.shields.io/pypi/l/django-sitetables.svg
    :target: https://pypi.python.org/pypi/django-sitetables

.. |ci| image:: https://img.shields.io/travis/idlesign/django-sitetables/master.svg
    :target: https://travis-ci.org/idlesign/django-sitetables

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/django-sitetables/master.svg
    :target: https://coveralls.io/r/idlesign/django-sitetables


**Work in progress. Stay tuned.**


Description
-----------

*Reusable application for Django featuring DataTables integration*

**Offers:**

* Various data sources support: models, query sets, list of dicts.
* ``DataTables`` plugins support: styling, internationalization, etc.
* Template tags for easy js and css inclusion.
* Template tags for DOM-based tables.


How to use
----------

First place table definition into ``views.py``:

.. code-block:: python

    from django.shortcuts import render
    from sitetables.toolbox import Table

    from .models import Entries


    def entries(request):
        # We create table from entries queryset,
        table_entries = Table(Entries.objects.filter(hidden=False))
        return render(request, 'entries.html', {'table_entries': table_entries})


Next create page template ``entries.html``:

.. code-block:: html

    {% load sitetables %}

    <!-- The following line usually goes into head tag. It'll load all needed css. -->
    {% sitetables_css table_entries %}

    <!-- The following resides in body tag. Note that in this scenario
         thead and tbody will be populated using JS automatically. -->
    <table id="table-entries"></table>

    <script type="text/javascript">
         $(function() {
             <!-- Initialize table using generated config. -->
             $('#table-entries').dataTable({% sitetable_config table_entries %});
         });
     </script>

    <!-- The following line usually goes somewhere near the end of the body.
         It'll load all needed js. -->
    {% sitetables_js table_entries %}


Done. *More information is available in the documentation.*


Documentation
-------------

http://django-sitetables.readthedocs.org/

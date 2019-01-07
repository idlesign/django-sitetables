from django.conf import settings


URL_CDN_BASE = getattr(settings, 'SITETABLES_URL_CDN_BASE', '//cdn.datatables.net/')

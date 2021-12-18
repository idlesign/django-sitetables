from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SitetablesConfig(AppConfig):
    """Application configuration."""

    name = 'sitetables'
    verbose_name = _('Sitetables')

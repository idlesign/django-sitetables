from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SitetablesConfig(AppConfig):
    """Application configuration."""

    name = 'sitetables'
    verbose_name = _('Sitetables')

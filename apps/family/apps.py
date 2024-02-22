from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FamilyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.family'
    verbose_name = _('Семья')

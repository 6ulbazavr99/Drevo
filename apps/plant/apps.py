from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.plant'
    verbose_name = _('Сад')

    def ready(self):
        import apps.plant.signals

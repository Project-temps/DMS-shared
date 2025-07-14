from django.apps import AppConfig
import logging


class UiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ui'

    def ready(self):
        import ui.dashapp
        logging.getLogger(__name__).info("UiConfig.ready: dashapp imported")

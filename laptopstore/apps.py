from django.apps import AppConfig


class LaptopstoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laptopstore'

    def ready(self):
        import laptopstore.signals

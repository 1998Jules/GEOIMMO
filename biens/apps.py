from django.apps import AppConfig


class BiensConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "biens"
    def ready(self):
        import biens.signals  # Assure-toi que ce chemin est correct

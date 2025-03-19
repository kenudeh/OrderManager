from django.apps import AppConfig


class LittleLemonApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LittleLemonAPI'


    def ready(self):
        import LittleLemonAPI.signals
from django.apps import AppConfig


class OrderManagerAPIConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OrderManagerAPI'


    def ready(self):
        import OrderManagerAPI.signals
        
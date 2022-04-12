from django.apps import AppConfig

from accesslog import mqtt


class PrintConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "print"

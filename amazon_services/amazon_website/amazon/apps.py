from django.apps import AppConfig

#Register the application's files in settings.py.
class AmazonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'amazon'

from django.apps import AppConfig


class PokeroleAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pokerole_app'

    # Overrige the ready function to import users.signals on startup
    def ready(self):
        import pokerole_app.signals

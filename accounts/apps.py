from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # overwrite ready 
    def ready(self):
        import accounts.signals

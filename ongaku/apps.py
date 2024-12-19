from django.apps import AppConfig


class OngakuConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ongaku"


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # signals.py をインポートしてシグナルを有効化

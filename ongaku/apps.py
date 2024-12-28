from django.apps import AppConfig


class OngakuConfig(AppConfig):
    name = 'ongaku'
    def ready(self):
        import ongaku.signals  # signalsがある場合など



class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # signals.py をインポートしてシグナルを有効化

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import your_app.signals

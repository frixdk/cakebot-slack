from django.apps import AppConfig
from django.db.models.signals import post_save


class BotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        from bot.signals import create_user_cake_ratio
        from django.contrib.auth.models import User
        post_save.connect(create_user_cake_ratio, sender=User)

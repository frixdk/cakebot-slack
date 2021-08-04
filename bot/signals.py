from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from bot.models import CakeRatio


@receiver(post_save, sender=User)
def create_user_cake_ratio(sender, instance, created, **kwargs):
    if created:
        CakeRatio.objects.create(user=instance, ratio=0.0)

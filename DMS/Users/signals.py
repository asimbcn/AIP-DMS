from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserInfo


def user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(
            user=instance,
            name=instance.first_name,
            email=instance.email,
        )


post_save.connect(user_profile, sender=User)
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

CURRENT_DATE = datetime.now()

# Create your models here.
class UserInfo(models.Model):
    groupchoices = models.TextChoices('groupchoices', 'management accounting sales tech')
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE,
                                null=True, 
                                blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200,null=True)
    image = models.ImageField(null=True, upload_to='profile_pics/')
    active = models.BooleanField(default=True)
    priv_level = models.IntegerField(default=3)
    group = models.CharField(max_length=100,
                             default='tech',
                             choices=groupchoices.choices)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/media/placeholder.png'

        return url
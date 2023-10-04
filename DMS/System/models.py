from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime, timedelta

# CURRENT_DATE = datetime.now()
# VALID = datetime.now() + timedelta(days=15)

# Create your models here.

class Files(models.Model):
    groupchoices = models.TextChoices('groupchoices', 'management all accounting sales tech')

    name = models.CharField(max_length=100)
    org_name = models.CharField(max_length=100, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    file = models.FileField(upload_to='files/')

    group = models.CharField(max_length=100,
                             default='all',
                             choices=groupchoices.choices)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    version = models.IntegerField(default='1')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    new_version = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @property
    def fileURL(self):
        try:
            url = self.file.url
        except:
            url = None

        return url
    
    @property
    def file_version(self):

        ver = self.version
        return ver        
    
class Version_control(models.Model):

    groupchoices = models.TextChoices('groupchoices', 'management all accounting sales tech')

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/version/')
    org_name = models.CharField(max_length=100, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    version = models.IntegerField(default='2')
    prev_version = models.ForeignKey(Files, on_delete=models.SET_NULL, null=True, blank=True)
    pre_ver_control = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.CharField(max_length=100,
                             default='all',
                             choices=groupchoices.choices)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    new_version = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @property
    def fileURL(self):
        try:
            url = self.file.url
        except:
            url = None

        return url


from django.db import models
from django.contrib.auth.models import User


class Developers(models.Model):
    nickname = models.CharField(max_length=255)
    avatar_url = models.URLField(blank=True) 
    users = models.ManyToManyField(User, through='DeveloperSubscribtions', related_name='developer_subscribes')


class DeveloperSubscribtions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

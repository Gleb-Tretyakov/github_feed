from django.db import models
from django.contrib.auth.models import User


class Developers(models.Model):
    nickname = models.CharField(max_length=255)
    avatar_url = models.URLField(blank=True) 
    users = models.ManyToManyField(User, through='DeveloperSubscriptions', related_name='developer_subscribes')


class DeveloperSubscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

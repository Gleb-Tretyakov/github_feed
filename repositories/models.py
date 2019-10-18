from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from branches.models import Branches


class Repositories(models.Model):
    name = models.CharField(max_length=255)
    stars = models.IntegerField()
    pulse_stats = JSONField()
    branches = models.ManyToManyField(Branches)
    users = models.ManyToManyField(User, through='RepositorySubscriptions', related_name='repository_subscribes')


class RepositorySubscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repositories, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

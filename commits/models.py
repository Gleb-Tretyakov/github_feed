from django.db import models
from django.contrib.auth.models import User
from developers.models import Developers
from django.contrib.postgres.fields import ArrayField
from branches.models import Branches


class Commits(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateField()
    developers = models.ManyToManyField(Developers)
    branches = models.ManyToManyField(Branches)
    message = models.CharField(max_length=1024)
    changed_fields = ArrayField(models.CharField(max_length=4096), blank=True)
    users = models.ManyToManyField(User, through='CommitUpdates', related_name='commit_updates')


class CommitUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commit = models.ForeignKey(Commits, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

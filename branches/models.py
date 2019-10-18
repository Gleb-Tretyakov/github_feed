from django.db import models
from django.contrib.auth.models import User


class Branches(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through='BranchUpdates', related_name='branch_updates')


class BranchUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

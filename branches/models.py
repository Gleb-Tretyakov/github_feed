from django.db import models
from django.contrib.auth.models import User


class Branches(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through='BranchUpdates', related_name='branch_updates')

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Branches.DoesNotExist:
            return None


class BranchUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

from django.db import models
from django.contrib.auth.models import User
from developers.models import Developers
from django.contrib.postgres.fields import ArrayField
from branches.models import Branches
from repositories.models import Repositories


class Commits(models.Model):
    creation_date = models.DateField()
    developers = models.ManyToManyField(Developers)
    repository = models.ManyToManyField(Repositories)
    branches = models.ManyToManyField(Branches)
    message = models.CharField(max_length=8192)
    changed_files = ArrayField(models.CharField(max_length=4096), blank=True)
    users = models.ManyToManyField(User, through='CommitUpdates', related_name='commit_updates')
    github_id = models.CharField(max_length=1024)

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Commits.DoesNotExist:
            return None


class CommitUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commit = models.ForeignKey(Commits, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

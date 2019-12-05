from django.shortcuts import render
from github_client import scripts


def feed(request):
    commits = scripts.feed_for_user(request.user)
    return render(request, 'feed.html', {'commits': commits})

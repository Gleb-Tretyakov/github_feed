from django.shortcuts import render, redirect
from github_client import scripts
from django.urls import reverse


def index(request):
    return render(request, 'repositories/repositories.html')


def search_repositories(r):
    form = {
        'repository_name': r.GET.get('repository_name', ''),
        'add_repository': r.GET.get('add_repository', ''),
        'rm_repository': r.GET.get('rm_repository', ''),
    }

    if form['add_repository']:
        scripts.add_repository_to_user(form['add_repository'], r.user)
        return redirect("%s?repository_name=%s" % (reverse('repositories:search_repositories'), form['repository_name']))

    if form['rm_repository']:
        scripts.delete_repository_from_user(form['rm_repository'], r.user)
        return redirect("%s?repository_name=%s" % (reverse('repositories:search_repositories'), form['repository_name']))

    search_result = scripts.search_repository(r.user, form['repository_name'])

    return render(r, 'repositories/search_repositories.html', {'form': form, 'search_result': search_result})


def favorite_repositories(r):
    form = {
        'rm_repository': r.GET.get('rm_repository', ''),
    }

    if form['rm_repository']:
        scripts.delete_repository_from_user(form['rm_repository'], r.user)
        return redirect(reverse('repositories:favorite_repositories'))

    fav_repositories = scripts.repository_subscriptions_of_user(r.user)

    return render(r, 'repositories/favorite_repositories.html', {'favorite_repositories': fav_repositories})

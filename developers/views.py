from django.shortcuts import render, render_to_response, redirect, reverse, redirect
from github_client import scripts
from django.urls import reverse


def index(request):
    return render(request, 'developers/developers.html')


def search_developers(r):
    form = {
        'developer_name': r.GET.get('developer_name', ''),
        'add_developer': r.GET.get('add_developer', ''),
        'rm_developer': r.GET.get('rm_developer', ''),
    }
    return render(request, 'developers/search_developers.html')

    if form['add_developer']:
        scripts.add_developer_to_user(form['add_developer'], r.user)
        return redirect("%s?developer_name=%s" % (reverse('developers:search_developers'), form['developer_name']))

    if form['rm_developer']:
        scripts.delete_developer_from_user(form['rm_developer'], r.user)
        return redirect("%s?developer_name=%s" % (reverse('developers:search_developers'), form['developer_name']))

    search_result = scripts.search_developer(r.user, form['developer_name'])

    return render(r, 'developers/search_developers.html', {'form': form, 'search_result': search_result})


def favorite_developers(r):
    form = {
        'rm_developer': r.GET.get('rm_developer', ''),
    }

    if form['rm_developer']:
        scripts.delete_developer_from_user(form['rm_developer'], r.user)
        return redirect(reverse('developers:favorite_developers'))

    fav_developers = scripts.preferences_of_user(r.user)

    return render(r, 'developers/favorite_developers.html', {'favorite_developers': fav_developers})


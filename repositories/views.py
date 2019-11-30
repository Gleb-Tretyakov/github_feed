from django.shortcuts import render


def index(request):
    return render(request, 'repositories/repositories.html')


def search_repositories(request):
    return render(request, 'repositories/search_repositories.html')


def favorite_repositories(request):
    return render(request, 'repositories/favorite_repositories.html')

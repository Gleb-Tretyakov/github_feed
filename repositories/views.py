from django.shortcuts import render


def index(request):
    return render(request, 'repositories/repositories.html')


def search_repositories(request):
    pass


def favorite_repositories(request):
    pass

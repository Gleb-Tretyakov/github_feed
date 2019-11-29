from django.shortcuts import render


def index(request):
    return render(request, 'developers/developers.html')


def search_developers(request):
    pass


def favorite_developers(request):
    pass

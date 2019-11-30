from django.shortcuts import render


def index(request):
    return render(request, 'developers/developers.html')


def search_developers(request):
    return render(request, 'developers/search_developers.html')


def favorite_developers(request):
    return render(request, 'developers/favorite_developers.html')

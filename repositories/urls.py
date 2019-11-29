from django.conf.urls import url
from . import views

app_name = 'repositories'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_repositories', views.search_repositories, name='search_repositories'),
    url(r'^favorite_repositories', views.favorite_repositories, name='favorite_repositories'),
]
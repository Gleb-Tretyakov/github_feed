from django.conf.urls import url
from . import views

app_name = 'developers'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_developers', views.search_developers, name='search_developers'),
    url(r'^favorite_developers', views.favorite_developers, name='favorite_developers'),
]
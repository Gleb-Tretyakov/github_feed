from django.conf.urls import url
from . import views

app_name = 'repositories'
urlpatterns = [
    url(r'^feed', views.feed, name='feed'),
]

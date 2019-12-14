"""github_feed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from profiles import views as profiles_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', profiles_views.home, name='home'),
    url(r'^feed/',  views.feed, name='feed'),
    url(r'^statistics/',  views.statistics, name='statistics'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', profiles_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^developers/', include('developers.urls')),
    url(r'^repositories/', include('repositories.urls')),
]

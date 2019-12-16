"""sea URL Configuration

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

from front.views import showmain, home, my_logout, continue_game, giveup

urlpatterns = [
    path("", showmain, name="main"),
    path("logout/", my_logout, name="logout"),
    path("home/", home, name="home"),
    path("game/<int:game_id>", continue_game, name="game"),
    path("giveup/<int:game_id>", giveup, name="giveup"),
    path('aa/<slug:title>/', showmain, name='article-detail'),
    path('admin/', admin.site.urls),
]

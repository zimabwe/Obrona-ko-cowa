"""coderslab URL Configuration

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
from django.urls import path, re_path
from exercises_app.views import *
from football.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', get_articles),
    path('show_band/<int:id>/', show_band),
    path('table/', league_table),
    path('number/', numbers),
    path('tabliczka/', multiplication_table),
    path('games/', games_played),
    path('celc/', cel_far),
    path('add-game/', add_game),
    path('set_session/', set_session),
    path('show_session/', show_session),
    path('delete_session/', delete_session),
    path('login/', login),
    path('addses/', add_to_session),
    path('show_all_session/', show_all_session),
    path('set_cookie/', set_cookie),
    path('show_cookie/', show_cookie),
    path('delete_cookie',delete_cookie),
    path('add_to_cookie/', add_to_cookie),
    path('show_all_session_cookie/', show_all_session_cookie),
    path('set_as_favourite/', set_as_favourite),
    path('newname/', NameForm.as_view()),
    path('calc/', Newcelcius.as_view()),
    path('addteam/', AddBand.as_view())
]

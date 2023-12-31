"""
URL configuration for dietetyk_projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from panel.views import base, register_pacjent, login_pacjent, panel_pacjenta, panel_dietetyka, strona_glowna, pobierz_diete


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base, name='home'),
    path('panel/', include('panel.urls')),
    path('login/', login_pacjent, name='login'),
    path('rejestracja/', register_pacjent, name='rejestracja'),
    path('panel_pacjenta/', panel_pacjenta, name='panel_pacjenta'),
    path('panel_dietetyka/', panel_dietetyka, name='panel_dietetyka'),
    path('strona_glowna/', strona_glowna, name='strona_glowna'),
    path('pobierz_diete/<int:diet_id>/', pobierz_diete, name='pobierz_diete'),
]

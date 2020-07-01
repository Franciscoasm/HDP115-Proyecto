"""ardc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from core import views as core_views
from agregar import views as agregar_views

from django.conf.urls import url
from core.ajax import get_municipios

urlpatterns = [
    # Paths del core
    path('', core_views.filtrar, name = "Filtrar"),
    path('agregar/', agregar_views.agregar, name = "Agregar Infromacion"),
    path('iniciar/', core_views.iniciar, name = "Iniciar Sesion"),
    # Admin
    path('admin/', admin.site.urls),
    url(r'ajax/get_municipios/', get_municipios, name='get_municipios'),
]

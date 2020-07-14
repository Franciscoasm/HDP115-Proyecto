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
from django.urls import path, include
from core import views
from django.conf.urls import url
from core.ajax import get_municipios, get_info

urlpatterns = [
    #Paths del core
    path('', views.filtrar, name = "Filtrar"),
    path('agregar/',views.agregar, name = "Agregar Infromacion"),
    #path('iniciar/', views.iniciar, name = "Iniciar Sesion"),
    #Admin
    path('admin/', admin.site.urls),
    url(r'ajax/get_municipios', get_municipios, name='get_municipios'),
    url(r'ajax/get_info', get_info, name='get_info'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('iniciar/', views.login, name = "Iniciar Sesion"),
    path('logout/', views.logout),
    path('welcome/', views.welcome)
]

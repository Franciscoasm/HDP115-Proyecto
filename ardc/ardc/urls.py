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
from core import views
from django.conf.urls import url
from core.ajax import get_municipios, get_info, get_last, get_detalle

urlpatterns = [
    #Paths del core
    path('', views.filtrar, name = "Filtrar"),
    path('agregar/',views.agregar, name = "Agregar Infromacion"),
    path('detalle/',views.detalleBeneficiario, name = "Agregar Ayuda"),
    path('actualizar/', views.actualizar, name = "actualizar"),
    path('iniciar/', views.iniciar, name = "Iniciar Sesion"),
    #Admin
    path('admin/', admin.site.urls),
    url(r'ajax/get_municipios', get_municipios, name='get_municipios'),
    url(r'ajax/get_info', get_info, name='get_info'),
    url(r'ajax/get_last', get_last, name='get_last'),
    url(r'ajax/get_detalle', get_detalle, name='get_detalle'),
]

from django.urls import path, include
from apps.core.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'index$',index),
    url(r'IniciarSesion$',IniciarSesion),
]
from django.urls import path, include
from apps.core.views import index
from django.conf.urls import url

urlpatterns = [
    url(r'$', index),
]
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('keepalive/', keepalive, name='keepalive'),

    path('', Dashboard.as_view(), name='dashboard'),
    path('historico/', Historico.as_view(), name='historico'),
    path('report/', Report.as_view(), name='report'),
]
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import VerificaVeiculo

urlpatterns = [
    path('', VerificaVeiculo.as_view(), name='vendedor_verifica'),
]
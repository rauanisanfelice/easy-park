from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import VerificaVeiculo, VenderCreditos

urlpatterns = [
    path('', VerificaVeiculo.as_view(), name='verifica_veiculo'),
    path('vender/', VenderCreditos.as_view(), name='vender_creditos'),
]
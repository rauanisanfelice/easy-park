from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('home/', Home.as_view(), name='home'),
    path('signup/', SignUp.as_view(), name='signup'),
    
    path('perfil/', PagePerfil.as_view(), name='perfil'),
    path('informacoes/', PageInformacoes.as_view(), name='info'),
    path('notificacoes/', PageNotificacoes.as_view(), name='notificacoes'),
    path('historico/', PageHistorico.as_view(), name='historico'),
    path('estacionar/', PageEstacionar.as_view(), name='estacionar'),
    path('veiculo/', PageVeiculo.as_view(), name='veiculo'),
    path('carteira/', PageCarteira.as_view(), name='carteira'),
    path('comprar/', PageComprar.as_view(), name='comprar'),
]
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('home/', Home.as_view(), name='home'),
    path('signup/', SignUp.as_view(), name='signup'),
    
    path('perfil/', Perfil.as_view(), name='perfil'),
    path('informacoes/', Informacoes.as_view(), name='info'),
    path('notificacoes/', Notificacoes.as_view(), name='notificacoes'),
]
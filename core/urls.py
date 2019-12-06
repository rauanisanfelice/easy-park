from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('usuario.urls')),
    path('administrativo/', include('administrativo.urls')),
    path('estacionamento/', include('estacionamento.urls')),
    path('vendedor/', include('vendedor.urls')),
    path('admin/', admin.site.urls),
]

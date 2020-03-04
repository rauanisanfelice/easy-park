from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('account/', include('django.contrib.auth.urls'), name='login'),

    path('', include('usuario.urls')),
    path('administrativo/', include('administrativo.urls')),
    path('vendedor/', include('vendedor.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('grabados/', include('apps.grabados.urls')),
    path('tintas/', include('apps.tintas.urls')),
    path('almacen/', include('apps.almacen.urls')),
    path('accounts/', include('apps.users.urls')),
]

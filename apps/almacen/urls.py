from django.urls import path
from .views import almacen_view

urlpatterns = [
    path('', almacen_view, name='almacen'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consulta/', views.grabado_consulta, name='grabado_consulta'),
    path('importar/', views.importar_from_upload_view, name='importar_upload'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('crear/', views.grabado_crear, name='grabado_crear'),
]
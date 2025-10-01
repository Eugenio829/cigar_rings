from django.contrib import admin
from .models import Grabado, Proceso, TipoGrabado, Maquina

@admin.register(Grabado)
class GrabadoAdmin(admin.ModelAdmin):
    list_display = ('of_referencia', 'cliente', 'estado', 'maquina', 'fecha_programacion')
    list_filter = ('estado', 'maquina', 'proceso', 'tipo_grabado', 'fecha_programacion')
    search_fields = ('of_referencia', 'cliente', 'descripcion')
    date_hierarchy = 'fecha_programacion'

@admin.register(Proceso)
class ProcesoAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(TipoGrabado)
class TipoGrabadoAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
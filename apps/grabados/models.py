from django.db import models

class Proceso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

class TipoGrabado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

class Maquina(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

class Grabado(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    of_numero = models.IntegerField(primary_key=True, verbose_name='OF.')
    of_referencia = models.CharField(max_length=100, unique=True, verbose_name='OF. Referencia')
    descripcion = models.TextField(verbose_name='Descripción')
    cliente = models.CharField(max_length=255, verbose_name='Cliente')
    
    tipo_grabado = models.ForeignKey(TipoGrabado, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo de Grabado')
    proceso = models.ForeignKey(Proceso, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Proceso')
    maquina = models.ForeignKey(Maquina, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Máquina')
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name='Estado')
    fecha_programacion = models.DateField(verbose_name='Fecha de Programación')
    ubicacion = models.CharField(max_length=255, verbose_name='Ubicación', blank=True)
    ubicacion_carpeta = models.CharField(max_length=255, verbose_name='Ubicación Carpeta', blank=True)

    def __str__(self):
        return self.of_referencia

    class Meta:
        verbose_name = 'Grabado'
        verbose_name_plural = 'Grabados'
        ordering = ['-fecha_programacion']
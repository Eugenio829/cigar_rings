from django import forms
from .models import Grabado

class GrabadoForm(forms.ModelForm):
    class Meta:
        model = Grabado
        fields = [
            'of_numero',
            'of_referencia',
            'cliente',
            'descripcion',
            'tipo_grabado',
            'proceso',
            'maquina',
            'estado',
            'fecha_programacion',
            'ubicacion',
            'ubicacion_carpeta',
        ]
        widgets = {
            'fecha_programacion': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.errors:
            field = self.fields.get(field_name)
            if field:
                # Add the is-invalid class to the widget
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_classes} is-invalid'.strip()

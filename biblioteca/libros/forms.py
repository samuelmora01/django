from django import forms
from .models import LibroFisico, LibroDigital

# Formulario para el libro físico
class LibroFisicoForm(forms.ModelForm):
    class Meta:
        model = LibroFisico
        fields = ['titulo', 'autor', 'anio_publicacion', 'num_paginas']

# Formulario para el libro digital
class LibroDigitalForm(forms.ModelForm):
    class Meta:
        model = LibroDigital
        fields = ['titulo', 'autor', 'anio_publicacion', 'formato', 'tamanio_mb']

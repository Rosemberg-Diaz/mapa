import datetime

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

'''Esta variable es una lista de tuplas que representan diferentes modos de transporte.
 Cada tupla contiene un nombre de visualización y un valor correspondiente.'''
mode_of_transport = [
    ("Driving", "driving"),
    ("Bicycling", "bicycling"),
    ("Walking", "walking"),
    ("Transit", "transit"),
]

''' Esta clase es una subclase de forms.DateTimeInput de Django y se utiliza para personalizar 
el tipo de entrada para los campos de fecha y hora en los formularios.'''
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

''' Este formulario está asociado con el modelo Empresas y define los campos y sus widgets correspondientes. 
Los campos incluyen NIT, nombre, mision, vision, descripcion, telefono, direccion, email y paginaWeb.
 A cada campo se le asigna un widget que determina cómo se muestra en el formulario HTML.'''
class empresaForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ('NIT', 'nombre', 'mision', 'vision', 'descripcion', 'telefono', 'direccion', 'email', 'paginaWeb')
        widgets = {
            'NIT': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'mision': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,  # número de filas del textarea
                    'cols': 40  # número de columnas del textarea
                }
            ),
            'vision': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,  # número de filas del textarea
                    'cols': 40  # número de columnas del textarea
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,  # número de filas del textarea
                    'cols': 40  # número de columnas del textarea
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'telefono': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'paginaWeb': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }

''' Este formulario está asociado con el modelo Servicios y contiene un único campo, nombre, con su correspondiente widget.'''
class serviciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
'''Este formulario está asociado con el modelo Especialidades y también contiene un único campo, nombre,
 con su correspondiente widget.'''
class especialidadesForm(forms.ModelForm):
    class Meta:
        model = Especialidades
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


'''Este formulario está asociado con el modelo Sedes y define los campos nombre, telefono y direccion, 
junto con sus widgets correspondientes.'''
class sedeForm(forms.ModelForm):
    class Meta:
        model = Sedes
        fields = ('nombre', 'telefono', 'direccion')
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'telefono': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

'''Este formulario está asociado con el modelo Empleados y define varios campos como 
nombres, apellidos, telefono, email, documento, cargo, experiencia y experienciaCargo, 
junto con sus widgets correspondientes.'''
class empleadoForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = ('nombres', 'apellidos', 'telefono', 'email',
                  'documento', 'cargo', 'experiencia', 'experienciaCargo')
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'experiencia': forms.TextInput(attrs={'class': 'form-control'}),
            'experienciaCargo': forms.TextInput(attrs={'class': 'form-control'}),
        }

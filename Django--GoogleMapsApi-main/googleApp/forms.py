import datetime

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

mode_of_transport = [
    ("Driving", "driving"),
    ("Bicycling", "bicycling"),
    ("Walking", "walking"),
    ("Transit", "transit"),
]


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


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

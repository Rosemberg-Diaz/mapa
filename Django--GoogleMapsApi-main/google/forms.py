import datetime

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

mode_of_transport = [
  ("Driving","driving"),
  ("Bicycling","bicycling"),
  ("Walking","walking"),
  ("Transit","transit"),
]


class DateTimeInput(forms.DateTimeInput):
  input_type = 'datetime-local'


class empresaForm(forms.ModelForm):
  class Meta:
    model = Empresas
    fields = ('NIT', 'nombre', 'mision', 'vision', 'descripcion', 'telefono', 'direccion', 'email', 'paginaWeb')
    widgets = {
      'NIT': forms.NumberInput(
      ),
      'descripcion': forms.Textarea(
        attrs={
          'rows': 5,  # número de filas del textarea
          'cols': 40  # número de columnas del textarea
        }
      ),
      'email': forms.EmailInput(
      ),
      'telefono': forms.NumberInput(
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
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
    fields = ('NIT', 'nombre', 'mision', 'vision', 'direccion', 'descripcion', 'email', 'paginaWeb')

class empleadoForm(forms.ModelForm):
  class Meta:
    model = Empleados
    fields = ('nombres', 'apellidos', 'telefono', 'email', 'documento', 'cargo', 'estado','experiencia','experienciaCargo')



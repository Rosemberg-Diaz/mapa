import datetime

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


mode_of_transport = [
  ("Driving","driving"),
  ("Bicycling","bicycling"),
  ("Walking","walking"),
  ("Transit","transit"),
]

"""
    Personaliza la representación de un campo de fecha y hora en un formulario de Django
    utilizando un elemento input de tipo 'datetime-local'.
"""

class DateTimeInput(forms.DateTimeInput):
  input_type = 'datetime-local'


"""
    Formulario para el modelo Empresas.

    Define los campos que se incluirán en el formulario y los widgets
    que se utilizarán para renderizarlos. El objetivo principal de
    esta clase es proporcionar una forma fácil de crear y manipular
    formularios HTML para la creación o actualización de instancias
    de modelo.
"""

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

#class sedeForm(forms.ModelForm):
    #  class Meta:
    #model = Sedes
    #fields = ('nombre', 'telefono', 'direccion')
    #widgets = {
    #  'nombre': forms.TextInput(
    #    attrs={
    #      'class': 'form-control'
    #    }
    #  ),
    #  'telefono': forms.NumberInput(
    #    attrs={
    #      'class': 'form-control'
    #    }
    #  ),
    #  'direccion': forms.TextInput(
    #    attrs={
    #      'class': 'form-control'
    #    }
    #  ),
    #}

"""
  Define un formulario para la creación de instancias de la clase Empleados.
  
  Atributos:
  
  nombres (CharField): campo para el ingreso del nombre del empleado.
  apellidos (CharField): campo para el ingreso del apellido del empleado.
  telefono (CharField): campo para el ingreso del número de teléfono del empleado.
  email (EmailField): campo para el ingreso del correo electrónico del empleado.
  documento (CharField): campo para el ingreso del número de documento del empleado.
  cargo (CharField): campo para el ingreso del cargo del empleado.
  experiencia (CharField): campo para el ingreso de la experiencia del empleado.
  experienciaCargo (CharField): campo para el ingreso de la experiencia del empleado en el cargo actual.
  Widgets:
  
  TextInput: widget para el ingreso de texto.
  EmailInput: widget para el ingreso de correos electrónicos.
"""

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

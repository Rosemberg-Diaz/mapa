from .models import Usuarios

from django.shortcuts import redirect

'''Esta función es una función decoradora utilizada para proteger vistas o funciones en Django,
 asegurando que el usuario esté autenticado antes de permitir el acceso. '''
def user_login_required(function):
 def wrapper(request, login_url='login', *args, **kwargs):
  if not 'user_id' in request.session:
   return redirect(login_url)
  else:
   return function(request, *args, **kwargs)
 return wrapper
from django.contrib.auth.backends import BaseBackend
from .models import Usuarios
'''Esta clase es una implementación personalizada de un backend de autenticación en Django. 
Se utiliza para autenticar a los usuarios en función de su dirección de correo electrónico y contraseña.
 La función authenticate toma el objeto request, así como los argumentos email y contraseña. '''
class CustomAuthBackend(BaseBackend):

    def authenticate(self, request, email=None, contraseña=None, **kwargs):
        try:
            user = Usuarios.objects.get(email=email)
        except Usuarios.DoesNotExist:
            return None
        if user.check_password(contraseña):
            return user
        return None

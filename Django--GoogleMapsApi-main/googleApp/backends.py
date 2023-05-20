from django.contrib.auth.backends import BaseBackend
from .models import Usuarios

class CustomAuthBackend(BaseBackend):

    def authenticate(self, request, email=None, contraseña=None, **kwargs):
        try:
            user = Usuarios.objects.get(email=email)
        except Usuarios.DoesNotExist:
            return None
        if user.check_password(contraseña):
            return user
        return None

from djongo import models
from django.db import models as model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
'''El modelo Ciudades representa una ciudad con dos campos: _id y nombre. El campo _id es un campo de identificación único y nombre es el nombre de la ciudad.'''
class Ciudades(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ciudades'

    def __str__(self):
        return self.nombre
    
'''El modelo Empresas representa una empresa con varios campos, como NIT (número de identificación tributaria), 
nombre, descripcion, telefono, ciudad (que es una clave foránea que se relaciona con el modelo Ciudades), 
fechaFundacion, email, mision, vision, paginaWeb, estado, direccion, latitude y longitude (para la ubicación geográfica de la empresa en la api de google).'''
class Empresas(models.Model):
    NIT = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudades, on_delete=models.CASCADE)
    fechaFundacion = models.DateField()
    email = models.CharField(max_length=100)
    mision = models.TextField()
    vision = models.TextField()
    paginaWeb = models.CharField(max_length=500)
    estado = models.BooleanField(default=True)
    direccion = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'Empresas'

    def __str__(self):
        return str(self.latitude) + str(self.longitude)

#class Sedes(models.Model):
#    _id = models.ObjectIdField(primary_key=True)
#    nombre = models.CharField(max_length=100)
#    telefono = models.CharField(max_length=100)
#    direccion = models.CharField(max_length=100)
#    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
#    ciudad = models.ForeignKey(Ciudades, on_delete=models.CASCADE)
#    estado = models.BooleanField(default=True)
#    latitude = models.FloatField()
#    longitude = models.FloatField()

#    class Meta:
#        db_table = 'Sedes'

#    def __str__(self):
#        return str(self.latitude) + str(self.longitude)
'''El modelo Empleados representa un empleado de una empresa con campos como
 nombres, apellidos, experienciaCargo, tipoDoc, documento, cargo, estado, fechaNacimiento, experiencia,
 videoEntrevista, telefono, imagen, entrevista, permiso, email y empresa (que es una clave foránea que se relaciona con el modelo Empresas).'''
class Empleados(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    experienciaCargo = models.CharField(max_length=100,default='1')
    tipoDoc = models.CharField(max_length=100)
    documento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    experiencia = models.IntegerField(default=0)
    videoEntrevista = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    imagen = models.TextField(default="n")
    entrevista = models.TextField(default="n")
    permiso = models.TextField(default="n")
    email = models.EmailField()
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Empleados'

    def __str__(self):
        return self.nombres

'''El modelo CustomUserManager es un administrador personalizado para el modelo de usuario personalizado
. Define métodos para crear usuarios y superusuarios.'''
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, contraseña, **extra_fields):
        if not email:
            raise ValueError('El correo electronico debe ser ingresado')
        if not username:
            raise ValueError('El nombre de usuario debe ser ingresado')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            rol='Cliente',
            contraseña=contraseña,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, contraseña, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        user = self.create_user(
            username=username,
            email=email,
            contraseña=contraseña,
        )
        user.rol = 'Administrador'
        user.is_superuser = True
        user.save(using=self._db)
        return user

'''El modelo Usuarios es una implementación personalizada del modelo de usuario proporcionado por Django llamado AbstractBaseUser. Este modelo de usuario personalizado se utiliza para autenticación y gestión de usuarios en el sitio. Tiene campos como _id, username, contraseña, email y rol. El campo USERNAME_FIELD se establece en 'email' para autenticar a los usuarios utilizando su correo electrónico. 
También se define un administrador personalizado (CustomUserManager) para este modelo de usuario.
Además, el modelo Usuarios tiene métodos adicionales para verificar los permisos del usuario y para comprobar si el usuario es un administrador o un cliente.
'''

class Usuarios(AbstractBaseUser):
    _id = models.ObjectIdField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    contraseña = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20)
    USERNAME_FIELD = 'email'
    PASSWORD_FIELD = 'contraseña'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    password = None

    class Meta:
        db_table = 'Usuarios'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.rol == 'Administrador'

    @property
    def is_cliente(self):
        return self.rol == 'Cliente'

    def check_password(self, raw_password):
        if raw_password == self.contraseña:
            return True
        return False

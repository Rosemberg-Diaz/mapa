from djongo import models
from django.db import models as model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

"""
Modelo para representar una ciudad en una base de datos.

Atributos:
- _id (ObjectIdField): Identificador único de la ciudad en la base de datos.
- nombre (CharField): Nombre de la ciudad.

Meta:
- db_table (str): Nombre de la tabla en la base de datos que almacena las ciudades.

Métodos:
- __str__(): Retorna el nombre de la ciudad como string.
"""
class Ciudades(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ciudades'

    def __str__(self):
        return self.nombre



"""
Modelo para representar una empresa en una base de datos.

Atributos:
- NIT (IntegerField): Identificador único de la empresa en la base de datos.
- nombre (CharField): Nombre de la empresa.
- descripcion (CharField): Descripción de la empresa.
- telefono (CharField): Número de teléfono de la empresa.
- ciudad (ForeignKey): Llave foránea que representa la ciudad en la que se encuentra la empresa.
- fechaFundacion (DateField): Fecha de fundación de la empresa.
- email (CharField): Correo electrónico de contacto de la empresa.
- mision (TextField): Misión de la empresa.
- vision (TextField): Visión de la empresa.
- paginaWeb (CharField): URL de la página web de la empresa.
- estado (BooleanField): Estado actual de la empresa.
- direccion (CharField): Dirección física de la empresa.
- latitude (FloatField): Coordenada de latitud de la ubicación de la empresa.
- longitude (FloatField): Coordenada de longitud de la ubicación de la empresa.

Meta:
- db_table (str): Nombre de la tabla en la base de datos que almacena las empresas.

Métodos:
- __str__(): Retorna la concatenación de la coordenada de latitud y longitud de la ubicación de la empresa.
"""

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

'''
Modelo para representar un empleado en una base de datos.

Atributos:
- nombres (CharField): Nombres del empleado.
- apellidos (CharField): Apellidos del empleado.
- experienciaCargo (CharField): Experiencia previa en el cargo del empleado.
- tipoDoc (CharField): Tipo de documento de identidad del empleado.
- documento (CharField): Número de documento de identidad del empleado.
- cargo (CharField): Cargo del empleado.
- estado (CharField): Estado actual del empleado.
- fechaNacimiento (DateField): Fecha de nacimiento del empleado.
- experiencia (IntegerField): Años de experiencia del empleado.
- videoEntrevista (CharField): URL del video de la entrevista del empleado.
- telefono (CharField): Número de teléfono del empleado.
- imagen (TextField): Imagen del empleado en formato base64.
- entrevista (TextField): Texto de la entrevista con el empleado.
- permiso (TextField): Permisos del empleado.
- email (EmailField): Correo electrónico del empleado.
- empresa (ForeignKey): Llave foránea que representa la empresa a la que pertenece el empleado.

Meta:
- db_table (str): Nombre de la tabla en la base de datos que almacena los empleados.

Métodos:
- __str__(): Retorna los nombres del empleado como string.
'''

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

"""
    Modelo de usuario personalizado que extiende AbstractBaseUser.

    Atributos:
    _id (ObjectIdField): campo para el ID del usuario
    username (CharField): nombre de usuario
    contraseña (CharField): contraseña del usuario
    email (EmailField): correo electrónico del usuario
    rol (CharField): rol del usuario (Administrador o Cliente)
    USERNAME_FIELD (str): nombre del campo utilizado para autenticar al usuario (email)
    PASSWORD_FIELD (str): nombre del campo utilizado para almacenar la contraseña
    REQUIRED_FIELDS (list): lista de campos requeridos al crear un usuario
    objects (CustomUserManager): objeto utilizado para manejar la creación de usuarios y superusuarios
    password: se establece en None para evitar el uso del campo heredado de AbstractBaseUser

    Métodos:
    __str__: devuelve el nombre de usuario del objeto
    has_perm: siempre devuelve True
    has_module_perms: siempre devuelve True
    is_admin: devuelve True si el usuario tiene el rol de Administrador
    is_cliente: devuelve True si el usuario tiene el rol de Cliente
    check_password: verifica si la contraseña proporcionada coincide con la del usuario
"""
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

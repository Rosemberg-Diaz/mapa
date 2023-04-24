from djongo import models

# Create your models here.

class Ciudades(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ciudades'

    def __str__(self):
        return self.nombre

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
        return self.nombre
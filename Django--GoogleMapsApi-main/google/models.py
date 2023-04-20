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
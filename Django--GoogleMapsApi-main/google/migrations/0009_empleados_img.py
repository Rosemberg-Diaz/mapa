# Generated by Django 2.2.14 on 2023-04-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0008_empleados_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleados',
            name='img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]

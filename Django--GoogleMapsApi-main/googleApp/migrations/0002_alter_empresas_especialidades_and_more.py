# Generated by Django 4.1.7 on 2023-05-24 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googleApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresas',
            name='especialidades',
            field=models.ManyToManyField(related_name='Empresas', to='googleApp.especialidades'),
        ),
        migrations.AlterField(
            model_name='empresas',
            name='servicios',
            field=models.ManyToManyField(related_name='Empresas', to='googleApp.servicios'),
        ),
    ]

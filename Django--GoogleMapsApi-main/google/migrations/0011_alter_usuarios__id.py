# Generated by Django 4.1.7 on 2023-04-26 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0010_alter_usuarios__id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

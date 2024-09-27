# Generated by Django 5.1.1 on 2024-09-25 22:21

import gestion_clientes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsignationModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('exclutions', 'EXCLUTION'), ('adds', 'ADD'), ('updates', 'UPDATE')], max_length=100)),
                ('registers', models.IntegerField()),
                ('file', models.FileField(upload_to=gestion_clientes.models.ruta_dinamica)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
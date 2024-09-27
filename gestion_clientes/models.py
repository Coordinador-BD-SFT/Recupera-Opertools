from pyspark.sql import SparkSession
from pyspark import errors as sparkerrors
from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from random import randint
import pandas as pd
import os
# Create your models here.


def ruta_dinamica(instance, filename):
    """
    Función para dinamizar el guardado de un archivo en base a su nombre

    Parámetros:
    instance -> models.Model: Instancia de un modelo que contenga un campo name.
    """
    if not instance.pk:
        path = f'files/upload/asignation/{instance.name}/{datetime.now()}.csv'
        return path.replace(':', '-')
    return filename


class AsignationModification(models.Model):
    modify_types = [
        ('exclutions', 'EXCLUTION'),
        ('adds', 'ADD'),
        ('updates', 'UPDATE'),
    ]

    name = models.CharField(max_length=100, choices=modify_types)
    registers = models.IntegerField(default=0)
    file = models.FileField(upload_to=ruta_dinamica)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=AsignationModification)
def _post_save_receiver(sender, instance, created, ** kwargs):
    if created:
        session = SparkSession.builder \
            .appName('count') \
            .getOrCreate()
        try:
            entry = session.read.csv(
                instance.file.path, header=True, inferSchema=True)
            print(entry.count())
            instance.registers = entry.count()
            instance.save(update_fields=['registers'])
        except Exception as err:
            print(f'Error al contar registros: {err}')
            instance.registers = 0
            instance.save(update_fields=['registers'])
        finally:
            pass
            # session.stop()


def count_registers(file):
    session = SparkSession.builder \
        .appName('count') \
        .getOrCreate()

    entry = session.read.csv(file, header=True, inferSchema=True)

    return entry.count()

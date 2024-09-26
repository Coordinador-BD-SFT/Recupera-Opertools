from pyspark.sql import SparkSession
from django.db import models
from datetime import datetime
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

    def save(self, *args, **kwargs):
        # self.registers = randint(500000, 2500000)

        # session = SparkSession.builder \
        #     .appName('count') \
        #     .getOrCreate()

        # entry = session.read.csv(self.file.path, header=True, inferSchema=True)

        # entry.show()
        # self.registers = entry.count()

        # session.stop()
        super().save(*args, **kwargs)

        fullpath = os.path.join(settings.MEDIA_ROOT, self.file.name)
        print(self.file.name, fullpath)

        entry = pd.read_csv(
            self.file.name,
            dtype=str
        )

        entry.head()

        self.registers = entry.count()

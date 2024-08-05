from django.db import models
from django.utils import timezone
from django.http import FileResponse
from utils.dataframes import whatsapp
from pathlib import Path
import pandas as pd
import os


# Create your models here.


class TipoReporte(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name


class Reporte(models.Model):
    campaigns_list = (
        ('mora_30', 'MORA 30'),
        ('especiales', 'ESPECIALES'),
        ('castigo', 'CASTIGO'),
    )
# Agregar campo de intervalo de numeros
    name = models.CharField(max_length=100)
    campaign = models.CharField(max_length=15, choices=campaigns_list)
    chats_file = models.FileField(upload_to='files/upload/chats/')
    envio_sms_file = models.FileField(
        upload_to='files/upload/sms_databases/')  # Campo a eliminar
    hora = models.TimeField()
    report_type = models.ForeignKey(
        TipoReporte, on_delete=models.CASCADE, to_field='name')
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name

    def crear_reporte(self):
        # Invocamos a database filter para filtrar los que hicieron match.
        reporte = whatsapp.data_base_filter(
            ['3203927995', '3207701556'],
            self.envio_sms_file,
            self.chats_file
        )

        # Asigamos los valores que retorna whatsapp.database_filter()
        filtered_base = reporte[0]
        no_encontrado = reporte[1]

        # Agregamos los numeros no encontrados a la columna
        numeros_append = pd.DataFrame({
            'Dato_Contacto': no_encontrado,
        })

        # Creamos una ruta para el archivo que se va a servir
        path = Path(f'files/download/{self.name}.xlsx')
        file_no_encontrado = pd.concat(
            [filtered_base, numeros_append], ignore_index=True)
        print(no_encontrado)
        final_file = file_no_encontrado.to_excel(path, index=False)
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=self.name)

    def save(self):
        if self.pk == None:
            self.crear_reporte()
        super().save()


# Modelo SMSBase: Modelo que almacenará todos los envios de mensajes que se hacen durante el mes
# categorizado por el tipo de reporte que se hace, es decir que el campo NAME sera unico, su
# relacion será con TipoReporte en el campo name (foreign key), tendra los campos name, tipo_reporte,
# sms_base, created_at; El objetivo de este modelo sera manejar las bases de datos, pudiendo
# actualizar diariamente, concatenando las bases que se le pasen.

class SMSBase(models.Model):
    sms_type = (
        ('mora_30', 'MORA 30'),
        ('especiales', 'ESPECIALES'),
        ('castigo', 'CASTIGO'),
        ('base_general', 'BASE GENERAL'),
    )

    tipo_reporte = models.ForeignKey(
        TipoReporte, on_delete=models.CASCADE, to_field='name')
    name = models.CharField(max_length=50, choices=sms_type)
    sms_base = models.FileField(upload_to='files/sms_databases')
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name

    def actualizar_base(self, nueva_base):
        # Logica para actualizar base aqui...
        return

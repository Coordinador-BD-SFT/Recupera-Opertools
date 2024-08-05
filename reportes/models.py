from django.db import models
from django.utils import timezone
from django.http import FileResponse
from utils.dataframes import whatsapp
from pathlib import Path
import pandas as pd
import os


# Create your models here.

# Modelo TipoReporte: Categoriza los tipos de reporte que maneja la app
class TipoReporte(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name


# Modelo Reporte: Se encarga de crear los reportes cruzando los archivos .xlsx (mas adelante .csv y .json)
class Reporte(models.Model):
    campaigns_list = (
        ('mora_30', 'MORA 30'),
        ('especiales', 'ESPECIALES'),
        ('castigo', 'CASTIGO'),
    )
    name = models.CharField(max_length=100)
    campaign = models.CharField(max_length=15, choices=campaigns_list)
    chats_file = models.FileField(upload_to='files/upload/chats/')
    numero_inicio = models.CharField(max_length=11)
    numero_final = models.CharField(max_length=11)
    hora = models.TimeField()
    report_type = models.ForeignKey(
        TipoReporte, on_delete=models.CASCADE, to_field='name')
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name

    def crear_reporte(self):
        # Invocamos a database filter para filtrar los que hicieron match.
        reporte = whatsapp.data_base_filter(
            [self.numero_inicio, self.numero_final],
            Path(f'files/upload/sms_databases/{self.campaign}/sms.xlsx'),
            self.chats_file,
        )

        # Obtenemos el dataframe con los que hicieron match
        filtered_base = reporte[0]

        # Creamos un dataframe con la lista retornada por reporte
        no_encontrado = reporte[1]
        numeros_append = pd.DataFrame({
            'Dato_Contacto': no_encontrado,
        })

        # Concatenamos los dataframes
        file_no_encontrado = pd.concat(
            [filtered_base, numeros_append], ignore_index=True)
        print(no_encontrado)

        # Creamos una ruta para el archivo que se va a servir
        path = Path(f'files/download/{self.name}.xlsx')
        final_file = file_no_encontrado.to_excel(path, index=False)
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=self.name)

    def save(self):
        if self.pk == None:
            self.crear_reporte()
        super().save()


# Modelo SMSBase: Se encarga de administrar las bases de datos de mensajes

# Funcion para dinamizar ruta de guardado
def ruta_dinamica(instance, filename):
    if not instance.pk:
        return f'files/upload/sms_databases/{instance.name}/sms.xlsx'


class SMSBase(models.Model):
    sms_type = (
        ('mora_30', 'MORA 30'),
        ('especiales', 'ESPECIALES'),
        ('castigo', 'CASTIGO'),
    )

    tipo_reporte = models.ForeignKey(
        TipoReporte, on_delete=models.CASCADE, to_field='name')
    name = models.CharField(max_length=50, choices=sms_type)
    sms_base = models.FileField(upload_to=ruta_dinamica)
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name

    def actualizar_base(self, nueva_base):
        # Creamos el dataframe de la base antigua
        if self.sms_base:
            df_antigua = pd.read_excel(self.sms_base.path)
        else:
            df_antigua = pd.DataFrame()

        # Concatenamos la nueva base con la antigua
        df_nueva = pd.read_excel(nueva_base.path)
        df_unido = pd.concat([df_antigua, df_nueva], ignore_index=True)

        # Limpiamos la base de los duplicados y la retornamos
        file = df_unido.drop_duplicates(keep='last')
        return file.to_excel(f'files/upload/sms_databases/{self.name}/sms.xlsx', index=False)

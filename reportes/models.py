from django.core.files.storage import default_storage
from utils.dataframes import whatsapp
from django.http import FileResponse
from django.utils import timezone
from django.db import models
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

        # probando agregar columna No encontrado
        print(len(no_encontrado))
        lon = len(no_encontrado)
        marca = ['zNO EXISTE'] * lon
        cuenta = ['N/A'] * lon
        identificacion = ['N/A'] * lon

        numeros_append = pd.DataFrame({
            'Dato_Contacto': no_encontrado,
            'Edad_Mora': marca,
            'Cuenta_Next': cuenta,
            'Identificacion': identificacion,
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

    def limpiar_base(self):
        base = pd.read_excel(self.sms_base, usecols=[
            'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'], dtype=str)

    def actualizar_base(self, nueva_base):
        # Creamos los dataframes de las bases nueva y antigua
        old_base = pd.read_excel(self.sms_base, usecols=[
                                 'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'], dtype=str)
        new_base = pd.read_excel(nueva_base, usecols=[
                                 'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'], dtype=str)

        # Concatenamos la nueva base con la antigua
        df_unido = pd.concat([old_base, new_base], ignore_index=True)

        # Contamos duplicados para obtener informacion
        print(df_unido.duplicated().sum())

        # Limpiamos la base de los duplicados y la retornamos
        file = df_unido.drop_duplicates(keep='last')
        file.to_excel(
            f'files/upload/sms_databases/{self.name}/sms.xlsx', index=False)

    def save(self):
        if self.pk == None:
            self.limpiar_base()
        super().save()

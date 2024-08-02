from django.db import models
from django.utils import timezone
from django.http import FileResponse
from utils.dataframes import whatsapp
from pathlib import Path
import pandas as pd


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

    name = models.CharField(max_length=100)
    campaign = models.CharField(max_length=15, choices=campaigns_list)
    chats_file = models.FileField(upload_to='files/upload/chats/')
    envio_sms_file = models.FileField(upload_to='files/upload/envio_sms/')
    hora = models.TimeField()
    report_type = models.ForeignKey(
        TipoReporte, on_delete=models.CASCADE, to_field='name')
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name

    def crear_reporte(self):
        reporte = whatsapp.data_base_filter(
            ['3208310164', '3202673427'],
            self.envio_sms_file,
            self.chats_file
        )
        filtered_base = reporte[0]
        no_encontrado = reporte[1]
        path = Path(f'files/download/{self.name}.xlsx')
        file = filtered_base.to_excel(path, index=False)
        print(no_encontrado)
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=self.name)

    def save(self):
        if self.pk == None:
            self.crear_reporte()
        super().save()

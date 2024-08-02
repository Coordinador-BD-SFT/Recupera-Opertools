from django.db import models
from django.utils import timezone
from utils.dataframes import whatsapp

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
        print(whatsapp.chat_filter(
            ['3208310164', '3202673427'],
            self.chats_file
        ))

    def save(self):
        if self.pk == None:
            self.crear_reporte()
        super().save()

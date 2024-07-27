from django.db import models

# Create your models here.


class ReporteWhatsapp(models.Model):
    tipos_reporte = (
        ('mora_30', 'MORA 30'),
        ('especiales', 'ESPECIALES'),
        ('castigo', 'CASTIGO')
    )

    title = models.CharField(max_length=100)
    tipo_reporte = models.CharField(max_length=30, choices=tipos_reporte)
    chats = models.FileField(upload_to='files/chats')
    basedata = models.FileField(upload_to='files/bases/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def create_report(self):
        print('Wait a second, we\'re creating the report')

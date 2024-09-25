from django.db import models

# Create your models here.


def ruta_dinamica(instance):
    """
    Función para dinamizar el guardado de un archivo en base a su nombre

    Parámetros:
    instance -> models.Model: Instancia de un modelo que contenga un campo name.
    """
    if not instance.pk:
        return f'files/upload/asignation/{instance.name}/{instance.created_at}.csv'


class AsignationModification(models.Model):
    modify_types = [
        ('exclutions', 'EXCLUTION'),
        ('adds', 'ADD'),
        ('updates', 'UPDATE'),
    ]

    name = models.CharField(max_length=100, choices=modify_types)
    registers = models.IntegerField()
    file = models.FileField(
        upload_to=ruta_dinamica,
        max_length=100
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

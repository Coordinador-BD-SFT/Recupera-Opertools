from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from . import models

"""
En este archivo se definen las clases administrador las cuales permiten
manejar la informacion y las instancias de cada moelo que registremos dentro
de una subclase de admin.ModelAdmin
fields -> Se refiere a los campos del formulario que deben aparecer en el Admin Site
exclude -> Se refiere a los camops que debe excluir el formulario en el Admin Site
list_display -> Se refiere a los campos que se mostraran en la lista de instancias
    del modelo en el Admin Site
"""


# Register your models here.

class TipoReporteAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name', 'created_at')


class ReporteAdmin(admin.ModelAdmin):
    fields = ('campaign', 'name', 'chats_file', 'report_type', 'hora')
    list_display = ('id', 'name', 'campaign',
                    'report_type', 'hora', 'created_at')


class SMSBaseAdmin(admin.ModelAdmin):
    fields = ('tipo_reporte', 'name', 'sms_base')
    list_display = ('id', 'tipo_reporte', 'name', 'sms_base', 'created_at')


class UsuarioAdmin(UserAdmin):
    model = models.Usuario
    # fields = ('username', 'email', 'is_staff', 'first_name',
    #           'last_name', 'campaign')
    # list_display = ('id', 'username', 'email', 'is_staff', 'first_name',
    #                 'last_name', 'campaign', 'rank', 'points')


# Registramos las clases, con su modelo relacionado, en el sitio del Administrador
admin.site.register(models.TipoReporte, TipoReporteAdmin)
admin.site.register(models.SMSBase, SMSBaseAdmin)
admin.site.register(models.Reporte, ReporteAdmin)
admin.site.register(models.Usuario, UsuarioAdmin)

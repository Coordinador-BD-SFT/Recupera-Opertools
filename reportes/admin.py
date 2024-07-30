from django.contrib import admin
from . import models
# Register your models here.


class TipoReporteAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name', 'created_at')


class ReporteAdmin(admin.ModelAdmin):
    fields = ('name', 'campaign', 'chats_file',
              'envio_sms_file', 'report_type', 'hora')
    list_display = ('id', 'name', 'campaign',
                    'report_type', 'hora', 'created_at')


admin.site.register(models.TipoReporte, TipoReporteAdmin)
admin.site.register(models.Reporte, ReporteAdmin)

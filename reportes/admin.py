from django.contrib import admin
from . import models
# Register your models here.


class TipoReporteAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name', 'created_at')


class ReporteAdmin(admin.ModelAdmin):
    fields = ('name', 'campaign', 'chats_file', 'report_type', 'hora')
    list_display = ('id', 'name', 'campaign',
                    'report_type', 'hora', 'created_at')


class SMSBaseAdmin(admin.ModelAdmin):
    fields = ('tipo_reporte', 'name', 'sms_base')
    list_display = ('id', 'tipo_reporte', 'name', 'sms_base', 'created_at')


admin.site.register(models.TipoReporte, TipoReporteAdmin)
admin.site.register(models.SMSBase, SMSBaseAdmin)
admin.site.register(models.Reporte, ReporteAdmin)

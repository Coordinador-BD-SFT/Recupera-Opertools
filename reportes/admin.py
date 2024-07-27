from django.contrib import admin
from .models import ReporteWhatsapp
# Register your models here.


class ReporteWhatsappAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tipo_reporte', 'created_at')


admin.site.register(ReporteWhatsapp, ReporteWhatsappAdmin)

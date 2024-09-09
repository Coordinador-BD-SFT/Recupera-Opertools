from django.http import request
from django.shortcuts import reverse, redirect


def global_context(request):
    return {
        'sidebar_urls': {
            'reporte_wsp': reverse('reportes:crear', kwargs={'tipo_reporte_name': 'whatsapp'}),
            'sms_bases': reverse('reportes:sms_bases', kwargs={'tipo_reporte_name': 'whatsapp'}),
            'masivos_wsp': reverse('reportes:whatsapp_scraping'),
        },
    }

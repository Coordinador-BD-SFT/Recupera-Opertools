from django.http import request
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy


def global_context(request):
    return {
        'sidebar_urls': {
            'resources': reverse('reportes:resources'),
            'upload_lists': reverse('reportes:upload_lists'),
            'lists_resources': reverse('reportes:lists_resources'),
            'sms_resources': reverse('reportes:sms_resources'),
        },
        'succes': reverse_lazy('reportes:success')
    }

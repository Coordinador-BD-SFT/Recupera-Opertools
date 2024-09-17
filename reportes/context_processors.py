from django.http import request
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy


def global_context(request):
    return {
        'sidebar_urls': {
            'act_see_lists': reverse('reportes:update_lists'),
            'upload_lists': reverse('reportes:upload_lists'),
            'lists_reports': reverse('reportes:lists_reports'),
            'telematic_reports': reverse('reportes:reports_sms'),
        },
        'succes': reverse_lazy('reportes:success')
    }

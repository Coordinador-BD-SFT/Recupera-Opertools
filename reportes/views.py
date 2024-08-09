from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from utils.dataframes import whatsapp
from django.urls import reverse
from . import models
from io import BytesIO
from . import forms
import pandas as pd
import os
# Create your views here.


def index(request):
    tipos_reporte = models.TipoReporte.objects.all()

    return render(
        request,
        'index.html',
        context={'tipos_reporte': tipos_reporte}
    )


def reporte(request, tipo_reporte_name):
    reportes = models.Reporte.objects.filter(report_type=tipo_reporte_name)
    report_type = models.TipoReporte.objects.get(name=tipo_reporte_name)

    return render(
        request,
        'reportes.html',
        context={
            'reportes': reportes,
            'report_type': report_type,
        }
    )


def reporte_form(request, tipo_reporte_name):
    report_type = get_object_or_404(models.TipoReporte, name=tipo_reporte_name)
    if request.method == 'POST':
        form = forms.Reporteform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/reportes/{tipo_reporte_name}')
    else:
        form = forms.Reporteform()

    return render(
        request,
        'reporte_form.html',
        context={
            'form': form,
            'report_type': report_type,
        }
    )


def reporte_detalle(request, tipo_reporte_name, reporte_id):
    report_type = get_object_or_404(models.TipoReporte, name=tipo_reporte_name)
    reporte = get_object_or_404(models.Reporte, id=reporte_id)
    file_names = {
        'chats_file_name': os.path.basename(reporte.chats_file.name) if reporte.chats_file else 'No file',
    }

    return render(
        request,
        'reporte_detalle.html',
        context={
            'reporte': reporte,
            'report_type': report_type,
            'file_names': file_names
        }
    )


def reporte_download(request, tipo_reporte_name, reporte_id):
    report_type = get_object_or_404(models.TipoReporte, name=tipo_reporte_name)
    reporte = get_object_or_404(models.Reporte, pk=reporte_id)

    try:
        response = FileResponse(
            open(f'files/download/{reporte.name}.xlsx', 'rb'), as_attachment=True, filename=f'{reporte.name}.xlsx')
        response['Content-Type'] = 'application/octet-stream'
        return response
    except FileNotFoundError:
        raise Http404('Archivo no encontrado')


def sms_bases(request, tipo_reporte_name):
    report_type = models.TipoReporte.objects.get(name=tipo_reporte_name)
    sms_bases = models.SMSBase.objects.all()

    return render(
        request,
        'sms_bases.html',
        context={
            'report_type': report_type,
            'sms_bases': sms_bases,
        }
    )


def sms_base_update(request, report_type_name, sms_base_id):
    report_type = get_object_or_404(models.TipoReporte, name=report_type_name)
    sms_base = get_object_or_404(models.SMSBase, pk=sms_base_id)
    if request.method == 'POST':
        form = forms.SMSBaseUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['nueva_base']
            sms_base.actualizar_base(archivo)
            print(f'Base envio SMS {sms_base.name} actualizada con exito!')
            return HttpResponseRedirect(f'/reportes/{report_type_name}')

    else:
        form = forms.SMSBaseUpdateForm()

    return render(
        request,
        'sms_base_update.html',
        context={
            'form': form,
            'sms_base': sms_base,
            'report_type': report_type,
        }
    )


def sms_base_download(request, report_type_name, sms_base_id):
    report_type = get_object_or_404(models.TipoReporte, name=report_type_name)
    sms_base = get_object_or_404(models.SMSBase, pk=sms_base_id)

    try:
        file = pd.read_excel(sms_base.sms_base)
        response = FileResponse(
            open(sms_base.sms_base.path, 'rb'), as_attachment=True, filename=f'{sms_base.name}.xlsx')
        response['Content-Type'] = 'application/octet-stream'
        return response
    except FileNotFoundError as err:
        raise Http404('Archivo no encontrado')


def success(request):
    return HttpResponse('<h1>Proceso completado con exito</h1>')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from utils.dataframes import whatsapp
from django.urls import reverse
from . import models
from io import BytesIO
from . import forms
import pandas as pd
import os
from datetime import datetime
# Create your views here.


def index(request):
    # Vista de la raiz de la ruta de la app

    # Traemos todas las instancias de TipoReporte de la base de datos
    tipos_reporte = models.TipoReporte.objects.all()
    scrapers = models.Scraper.objects.all()

    # Renderizamos vista
    return render(
        request,
        'reportes/index.html',
        context={
            'tipos_reporte': tipos_reporte,
            'scrapers': scrapers,
        }
    )


def reporte(request, tipo_reporte_name):
    # Vista de la lista de instancias del modelo Reportes

    # Filtramos por tipo_reporte y ordenamos descendentemente con 5 instancias
    reportes = models.Reporte.objects.filter(
        report_type=tipo_reporte_name).order_by('-id')[:5]
    # Traemos las instancias necesarias desde la base de datos
    report_type = models.TipoReporte.objects.get(name=tipo_reporte_name)
    sms_bases = models.SMSBase.objects.all()

    # Renderizamos vista
    return render(
        request,
        'reportes/reportes.html',
        context={
            'reportes': reportes,
            'report_type': report_type,
            'sms_bases': sms_bases,
        }
    )


def reporte_form(request, tipo_reporte_name):
    # Vista del formulario para crear una instancia de Reporte

    # Usamos el manager para pasarle los argumentos necesarios a la URL
    report_type = get_object_or_404(models.TipoReporte, name=tipo_reporte_name)

    # Validamos el formulario
    if request.method == 'POST':
        form = forms.Reporteform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/reportes/{tipo_reporte_name}')
    else:
        form = forms.Reporteform()

    # Renderizamos vista
    return render(
        request,
        'reportes/reporte_form.html',
        context={
            'form': form,
            'report_type': report_type,
        }
    )


def reporte_detalle(request, tipo_reporte_name, reporte_id):
    # Vista del detalle de cada instancia de Rporte

    # Traemos informacion de la Base para la url y la vista
    report_type = get_object_or_404(models.TipoReporte, name=tipo_reporte_name)
    reporte = get_object_or_404(models.Reporte, id=reporte_id)
    chats_file_name = os.path.basename(
        reporte.chats_file.name) if reporte.chats_file else 'No file'

    # Renderizamos vista
    return render(
        request,
        'reportes/reporte_detalle.html',
        context={
            'reporte': reporte,
            'report_type': report_type,
            'file_names': chats_file_name
        }
    )


def reporte_download(request, tipo_reporte_name, reporte_id):
    # Vista controladora de la descarga del reporte de una instancia Reporte

    # Traemos informacion de la base de datos para la vista y la URL
    report_type = get_object_or_404(models.TipoReporte, name=tipo_reporte_name)
    reporte = get_object_or_404(models.Reporte, pk=reporte_id)

    # Manejamos la descarga con un try-except
    try:
        # Creamos una instancia de FileResponse y la agregamos a las descargas
        response = FileResponse(
            open(f'files/download/{reporte.name}', 'rb'),
            as_attachment=True,
            filename=reporte.name
        )
        response['Content-Type'] = 'application/octet-stream'
        return response
    except FileNotFoundError:
        # Si el archivo buscado no es encontrado manejamos la excepcion
        raise Http404('Archivo no encontrado')


def sms_bases(request, tipo_reporte_name):
    # Vista del listado de las bases de SMS

    # Obtenemos indormacion de la base de datos para la vista y la URL
    report_type = models.TipoReporte.objects.get(name=tipo_reporte_name)
    sms_bases = models.SMSBase.objects.all()

    # Renderizamos vista
    return render(
        request,
        'reportes/sms_bases.html',
        context={
            'report_type': report_type,
            'sms_bases': sms_bases,
        }
    )


def sms_base_update(request, report_type_name, sms_base_id):
    # Vista para actuaizar las bases de SMS

    # Obtenemos informacion de la base de datos para la vista y la URL
    report_type = get_object_or_404(models.TipoReporte, name=report_type_name)
    sms_base = get_object_or_404(models.SMSBase, pk=sms_base_id)

    # Validamos formulario
    if request.method == 'POST':
        form = forms.SMSBaseUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtenemos el archivo del formulario (nueva base)
            archivo = request.FILES['nueva_base']
            # Eejcutamos el metodo actualizar_base de la instancia
            sms_base.actualizar_base(archivo)
            print(f'Base envio SMS {sms_base.name} actualizada con exito!')
            return HttpResponseRedirect(f'/reportes/{report_type_name}')

    else:
        form = forms.SMSBaseUpdateForm()

    # Renderizamos vista
    return render(
        request,
        'reportes/sms_base_update.html',
        context={
            'form': form,
            'sms_base': sms_base,
            'report_type': report_type,
        }
    )


def sms_base_download(request, report_type_name, sms_base_id):
    # Vista que controla la descarga del archivo de registros de envio de SMS

    # Obtenemos informacion de la base de datos para la vista y la URL
    report_type = get_object_or_404(models.TipoReporte, name=report_type_name)
    sms_base = get_object_or_404(models.SMSBase, pk=sms_base_id)

    # Manejamos la descarga dentro de un ty-except
    try:
        # Leemos el archivo existente (old base)
        file = pd.read_excel(sms_base.sms_base)
        # Usamos la clase FileResponse para la descarga
        response = FileResponse(
            open(sms_base.sms_base.path, 'rb'), as_attachment=True, filename=f'{sms_base.name}.xlsx')
        response['Content-Type'] = 'application/octet-stream'
        return response
    except FileNotFoundError as err:
        # Si el archivo no es encontrado manejamos excepcion
        raise Http404('Archivo no encontrado')


def scrapers(request, scraper_id):
    scraper = get_object_or_404(models.Scraper, id=scraper_id)

    return render(
        request,
        'scrapper.html',
        context={
            'scraper': scraper,
        }
    )


def success(request):
    # Vista para retornar una vista de <¡exito!>
    return HttpResponse('<h1>Proceso completado con exito</h1>')

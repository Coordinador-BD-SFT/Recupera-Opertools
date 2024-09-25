from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from selenium.common import exceptions as selexceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.dataframes import whatsapp, churn
from utils.scrapping.common import get_driver, quit_driver
from utils.scrapping import whatsapp_scraper, vicidial_scraper
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from utils.dataframes import telematica
from datetime import datetime
from functools import reduce
from pathlib import Path
from . import models
from io import BytesIO
from . import forms
import pandas as pd
import math
import time
import os
# Create your views here.


def index(request):
    # Vista de la raiz de la ruta de la app

    # Traemos todas las instancias de TipoReporte de la base de datos
    tipos_reporte = models.TipoReporte.objects.all()
    # Renderizamos vista
    return render(
        request,
        'reportes/index.html',
        context={
            'tipos_reporte': tipos_reporte,
        }
    )


def tipos_reporte(request):
    tipos_reporte = models.TipoReporte.objects.all()

    return render(
        request,
        'reportes/tipos_reportes.html',
        context={
            'tipos_reporte': tipos_reporte,
        }
    )


def reporte(request, tipo_reporte_name):
    # Vista de la lista de instancias del modelo Reportes

    # Filtramos por tipo_reporte y ordenamos descendentemente con 5 instancias
    reportes = models.Reporte.objects.filter(
        report_type=tipo_reporte_name).order_by('-id')[:5]
    # Traemos las instancias necesarias desde la base de datos
    report_type = get_object_or_404(models.TipoReporte, name=tipo_reporte_name)
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


def resources(request):
    return render(
        request,
        'reportes/resources.html',
        # context=
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
            return HttpResponseRedirect(f'/reportes/reportes/{tipo_reporte_name}')
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


def files_and_bases(request):

    return render(
        request,
        'reportes/files&bases.html',
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
            url_response = reverse('reportes:reporte', kwargs={
                                   'tipo_reporte_name': report_type_name})
            return HttpResponseRedirect(url_response)

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
            open(sms_base.sms_base.path, 'rb'), as_attachment=True, filename=f'{sms_base.name}.csv')
        response['Content-Type'] = 'application/octet-stream'
        return response
    except FileNotFoundError as err:
        # Si el archivo no es encontrado manejamos excepcion
        raise Http404('Archivo no encontrado')


def whatsapp_scraping(request):
    # Vista que controla el envio masivo automatico de whatsapp
    if request.method == 'POST':
        form = forms.WhatsappScrapingForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtenemos el archivo con los numeros y mensajes y lo filtramos
            messages = form.cleaned_data['messages']
            verify_num = form.cleaned_data['nums_verify']

            df = churn.get_info(
                messages,
                ['Dato_Contacto', 'Cuenta', 'SMS'],
                os.path.splitext(messages.name)[-1]
            )

           # Definimos una funcion para aplicar a cada fila del dataframe
            def auto_send(row, driver):
                # Creamos el indice
                idx = row.name
                # Pausamos la operacion por 5 min cada 200 mensajes
                # if (int(idx) % 200) == 0:
                # time.sleep(300)
                try:
                    # Obtenemos el número y el mensaje
                    dato_contacto = row['Dato_Contacto']
                    mensaje = row['SMS']
                    # Buscamos el numero con selenium
                    is_wsp = whatsapp_scraper.search_num(driver, dato_contacto)
                    if is_wsp:
                        # Si existe, enviamos el mensaje (*) y modificamos el dataframe
                        if not verify_num:
                            whatsapp_scraper.send_msj(driver, mensaje)
                            df.at[idx, 'tipologia'] = 'ENVIADO'
                            enviados = len(df[df['tipologia'] == 'ENVIADO'])
                            print(
                                f'{idx} - {dato_contacto}, ENVIADO, {datetime.now()}\nEnviados: {enviados}')
                        else:
                            # Si solo estamos verificando numeros, llenamos el dataframe segun corresponda
                            df.at[idx, 'tipologia'] = 'Si Es Whatsapp'
                            print(
                                f'{idx} - {dato_contacto}, si es whatsapp, {datetime.now()}'
                            )
                        # Brindamos informacion en la terminal
                    else:
                        # Si no existe, modificamos el dataframe e imprimimos informacin en la terminal
                        df.at[idx, 'tipologia'] = 'No es WhatsApp'
                        print(
                            f'{idx} - {dato_contacto}, No es WhatsApp, {datetime.now()}')
                    # Rescribimos el dataframe en cada iteracion para no perder la información en caso de algún fallo
                    df.to_excel(
                        f'files/download/auto_wsp/Auto_Envio_wsp{messages.name}', index=False)

                except (Exception, selexceptions.NoSuchWindowException) as err:
                    print(
                        f'Ocurrio un error en el indice {idx}\nReiniciando proceso...\nError -> {err}')
                    # En caso de error, reiniciamos la funcion para no perder el indice en el que estabamos
                    driver.quit()
                    time.sleep(5)
                    driver = get_driver()
                    time.sleep(2)
                    whatsapp_scraper.get_whatsapp(driver)

                    # Reintentar iteracion
                    auto_send(row, driver)

            try:
                # Creamos una columna para mapear datos
                df['tipologia'] = [None] * len(df)
                driver = get_driver()
                # Navegamos a whatsapp web
                whatsapp_scraper.get_whatsapp(driver)

                # Ejecutamos una funcion para cada fila del dataframe (mas eficiente que un for)
                df.apply(lambda row: auto_send(row, driver), axis=1)

                quit_driver(driver)

                return HttpResponse(f'Proceso completado con exito!\nTotal de iteraciones -> {len(df)}')

            except Exception as err:
                print(f'Error -> {err}')

    else:
        form = forms.WhatsappScrapingForm()

    return render(
        request,
        'reportes/whatsapp_scraping.html',
        context={
            'form': form
        }
    )


def vicidial(request):

    return render(
        request,
        'reportes/vicidial.html'
    )


def clean_lists(request):
    # Definimos los links que visitara el scraper
    driver = get_driver()

    for link in request.vicidial_links.values():
        # Por cada link de listas ejecutamos la funcion
        vicidial_scraper.get_vicidial_lists(driver, url=link, metodo='clean')

    quit_driver(driver)

    return render(
        request,
        'success.html'
    )


def download_lists(request):
    driver = get_driver()

    for link in request.vicidial_links.values():
        # Por cada link de listas ejecutamos la función
        vicidial_scraper.get_vicidial_lists(
            driver, url=link, metodo='download'
        )

    quit_driver(driver)

    return render(
        request,
        'success.html'
    )


def upload_lists(request):
    # Obtenemos el navegador
    driver = get_driver()

    # Obtenemos la carpeta con las listas
    files_dir = Path('files/upload/listas')

    # Obtenemos ls links para montar las listas
    print('Cargando listas...')
    for link in request.vicidial_links.values():
        # Navegamos a la url e iniciamos sesión
        driver.get(link)
        vicidial_scraper.login_keys()
        # Obtenemos el modulo de listas
        lists_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[8]/td/a'
        )))
        lists_link.click()
        time.sleep(1)
        # Iteramos el directorio para subir los elmentos
        for file in files_dir.iterdir():
            # Condicionamos por tipo de lista
            if ('TRANS' in file.stem and '192.227.120.75' in link):
                print(f'Cargando {file.stem}...')
                # Logica para subir el archivo
                vicidial_scraper.upload_lists(driver, file)
            elif ('IVR' in file.stem and '192.227.124.58' in link):
                print(f'Cargando {file.stem}...')
                # logica para subir el archivo
                vicidial_scraper.upload_lists(driver, file)
            else:
                stems = ['IVR', 'TRANS']
                if not any(stem in file.stem for stem in stems):
                    print('El archivo no corresponde')
                else:
                    continue

    driver.quit()

    return render(
        request,
        'success.html'
    )


class UpdateLists(FormView):
    form_class = forms.UpdateListsForm
    template_name = 'reportes/update_lists.html'
    success_url = reverse_lazy('reportes:success')
    files_dir = Path('files/upload/listas')

    def form_valid(self, form):
        # files = form.cleaned_data['lists_files']
        files = self.request.FILES.getlist('lists_files')
        lists_dir = Path('files/upload/listas')
        for file in lists_dir.iterdir():
            os.remove(file)
        # Agregamos los nuevos
        for file in files:
            file_path = lists_dir / file.name
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inside_files"] = self.get_files(self.files_dir)
        return context

    def get_files(self, path):
        return [file.stem for file in path.iterdir()]


class UpdateSMSFiles(FormView):
    form_class = forms.UpdateSMSFilesForm
    template_name = 'reportes/update_sms_files.html'
    success_url = reverse_lazy('reportes:success')
    files_dir = Path('files/upload/envio_sms')

    def form_valid(self, form):
        # files = form.cleaned_data['lists_files']
        files = self.request.FILES.getlist('sms_files')
        sms_files_dir = Path('files/upload/envio_sms')
        for file in sms_files_dir.iterdir():
            os.remove(file)
        # Agregamos los nuevos
        for file in files:
            file_path = sms_files_dir / file.name
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inside_files"] = self.get_files(self.files_dir)
        return context

    def get_files(self, path):
        return [file.stem for file in path.iterdir()]


def lists_resources(request):
    # Funcion para renderizar reportes sobre las listas de IVRs y Transaccionales
    # Tomamos el tiempo en el que comienza la tarea
    start_time = time.time()
    # Referenciamos el directorio de las listas
    files_dir = Path('files/upload/listas')
    columna = 'FIRST NAME'
    values = {}
    total = 0

    if request.method == 'POST':
        print(f'Data recibida: {request.POST}')
        form = forms.ListsResourcesReportForm(request.POST)
        if form.is_valid():
            # Obtenemos el tipo de lista a iterar
            chanel = form.cleaned_data['channel']
            dataframe = telematica.read_lists(files_dir, chanel)
            values = telematica.count_reg_per_camppaign(dataframe, columna)
            total = reduce(lambda x, y: x + y.recuento, values, 0)
    else:
        form = forms.ListsResourcesReportForm()

    end_time = time.time()
    execution_time = end_time - start_time

    return render(
        request,
        'reportes/lists_resources.html',
        context={
            'form': form,
            'values': values,
            'execution_time': round(execution_time, 3),
            'total': total,
        }
    )


def sms_resources(request):
    start_time = time.time()

    files_dir = Path('files/upload/envio_sms')

    records = telematica.read_sms(files_dir)

    total = reduce(lambda x, y: x + y.recuento, records, 0)

    end_time = time.time()
    execution_time = end_time - start_time

    return render(
        request,
        'reportes/sms_resources.html',
        context={
            'records': records,
            'execution_time': round(execution_time, 3),
            'total': total,
        }
    )


def telematica_module(request):

    return render(
        request,
        'reportes/telematica.html',
    )


def success(request):
    # Vista para retornar una vista de <¡exito!>
    return render(
        request,
        'success.html'
    )

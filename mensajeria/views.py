import os
from datetime import datetime
import time
import pandas as pd
from . import forms
from utils.scrapping import whatsapp_scraper
from utils.scrapping.common import get_driver, quit_driver
from utils.dataframes import churn
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from selenium.common import exceptions as selexceptions
from selenium.common import exceptions as selexceptions

# Create your views here.


def index(request):
    return render(
        request,
        'mensajeria/index.html',
    )


def whatsapp_scraping(request):
    if request.method == 'POST':
        form = forms.WhatsappScrapingForm(request.POST, request.FILES)
        if form.is_valid():
            messages = form.cleaned_data['messages']
            df = churn.get_info(
                messages,
                ['Dato_Contacto', 'SMS'],
                os.path.splitext(messages.name)[1]
            )

            # def auto_send(row):
            def auto_send(row, driver, not_wsp):
                idx = row.name
                try:
                    dato_contacto = row['Dato_Contacto']
                    mensaje = row['SMS']
                    is_wsp = whatsapp_scraper.search_num(driver, dato_contacto)
                    # is_wsp = False if (idx % 30) == 0 else True
                    if is_wsp:
                        whatsapp_scraper.send_msj(driver, mensaje)
                        df.at[idx, 'tipologia'] = 'ENVIADO'
                        enviados = len(df[df['tipologia'] == 'ENVIADO'])
                        print(
                            f'{idx} - {dato_contacto}, ENVIADO, {datetime.now()}')
                        print(f'Enviados: {enviados}')
                    else:
                        df.at[idx, 'tipologia'] = 'No es WhatsApp'
                        not_wsp.append(dato_contacto)
                        # print(
                        #     f'Num: {dato_contacto} no es whatsapp - en la fila->{idx}')
                        print(
                            f'{idx} - {dato_contacto}, No es WhatsApp, {datetime.now()}')
                    df.to_excel(
                        f'files/download/auto_wsp/Auto_Envio_wsp{messages.name}', index=False)

                except (Exception, selexceptions.NoSuchWindowException) as err:
                    # except Exception as err:
                    print(
                        f'Ocurrio un error en el indice {idx}\nReiniciando proceso...\nError -> {err}')
                    driver.quit()
                    time.sleep(5)
                    driver = whatsapp_scraper.get_driver()
                    time.sleep(2)
                    whatsapp_scraper.get_whatsapp(driver)

                    # Reintentar iteracion
                    auto_send(row, driver, not_wsp)
                    # auto_send(row)

            try:
                not_wsp = []
                df['tipologia'] = [None] * len(df)
                driver = whatsapp_scraper.get_driver()
                whatsapp_scraper.get_whatsapp(driver)

                df.apply(lambda row: auto_send(row, driver, not_wsp), axis=1)
                # df.apply(auto_send, axis=1)

                whatsapp_scraper.quit_driver(driver)

                return HttpResponse(f'Proceso completado con exito!\nTotal de iteraciones -> {len(df)}')

            except Exception as err:
                print(f'Error -> {err}')

    else:
        form = forms.WhatsappScrapingForm()

    return render(
        request,
        'mensajeria/whatsapp_scraping.html',
        context={
            'form': form
        }
    )

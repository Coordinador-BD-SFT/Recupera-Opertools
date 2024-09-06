import os
import datetime
import pandas as pd
from . import forms
from utils.scrapping import whatsapp_scraper
from utils.scrapping.common import get_driver, quit_driver
from utils.dataframes import churn
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
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

            driver = get_driver()
            not_wsp = []
            yes_wsp = 0
            df['tipologia'] = [None] * len(df)

            try:
                for idx, row in df.iterrows():
                    whatsapp_scraper.get_whatsapp(driver)
                    dato_contacto = row['Dato_Contacto']
                    mensaje = row['SMS']
                    is_wsp = whatsapp_scraper.search_num(driver, dato_contacto)
                    if is_wsp[0]:
                        whatsapp_scraper.send_msj(driver, mensaje)
                        yes_wsp += 1
                        print(f'Mensajes enviados hasta el momento: {yes_wsp}')
                        df.at[idx, 'tipologia'] = 'ENVIADO'
                    else:
                        df.at[idx, 'tipologia'] = 'No es WhatsApp'
                    df.to_excel(
                        f'files/download/auto_wsp/Auto_Envio_wsp{messages.name}', index=False)
                    print(f'Total hasta ahora: {idx}')

                quit_driver(driver)

                return HttpResponse(f'Proceso completado con exito!\nColumnas iteradas -> {idx}\nMensajes enviados -> {yes_wsp}\nUltimo numero -> {dato_contacto}')

            except selexceptions.NoSuchWindowException:
                df.to_excel(
                    f'files/download/auto_wsp/Auto_Envio_wsp{messages.name}', index=False)
                return HttpResponse(f'Proceso Interrumpido')

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

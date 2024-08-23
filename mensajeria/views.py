import os
from . import forms
from utils.scrapping import vicidial_scraper
from utils.scrapping import whatsapp_scraper
from utils.dataframes import churn
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect

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

            # first_row = df.iloc[0]
            # dato_contacto = first_row['Dato_Contacto']
            # mensaje = first_row['SMS']

            driver = whatsapp_scraper.get_driver()
            not_wsp = []
            yes_wsp = 0
            total = 0

            try:
                for idx, row in df.iterrows():
                    row = list(row)
                    dato_contacto = row[0]
                    mensaje = row[1]
                    whatsapp_scraper.get_whatsapp(driver)
                    is_wsp = whatsapp_scraper.search_num(driver, dato_contacto)
                    if is_wsp[0]:
                        whatsapp_scraper.send_msj(driver, mensaje)
                        yes_wsp += 1
                        print(f'Mensajes enviados hasta el momento: {yes_wsp}')
                    else:
                        not_wsp.append(dato_contacto)
                    print(f'Total so far: {total}')

                whatsapp_scraper.quit_driver(driver)
                # for idx, row in df.iterrows():
                #     row = list(row)
                #     dato_contacto = row[0]
                #     mensaje = row[1]
                #     print(f'Registro -> {dato_contacto} | {mensaje}')

                # return HttpResponse(f'Proceso terminado.\nUltimo registro -> {dato_contacto} | {mensaje}')
                return f'Proceso Terminado.\nMensajes enviados ->{yes_wsp}\nNumeros que no poseen whatsapp -> {len(not_wsp)}'
            except Exception as err:
                print(f'Error -> {err}')

            return HttpResponse(f'Celular: {dato_contacto}\nMensaje: {mensaje} ')

    else:
        form = forms.WhatsappScrapingForm()

    return render(
        request,
        'mensajeria/whatsapp_scraping.html',
        context={
            'form': form
        }
    )

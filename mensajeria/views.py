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

            first_row = df.iloc[0]
            dato_contacto = first_row['Dato_Contacto']
            mensaje = first_row['SMS']

            driver = whatsapp_scraper.get_driver()

            try:
                whatsapp_scraper.get_whatsapp(driver)
                whatsapp_scraper.search_num(driver, dato_contacto)
                whatsapp_scraper.send_msj(driver, mensaje)
                whatsapp_scraper.quit_driver(driver)
            except Exception as err:
                print(f'Error -> {err}')

            # return HttpResponse(f'Celular: {dato_contacto}\nMensaje: {mensaje} ')

    else:
        form = forms.WhatsappScrapingForm()

    return render(
        request,
        'mensajeria/whatsapp_scraping.html',
        context={
            'form': form
        }
    )

from . import forms
from utils.scrapping import vicidial_scrapper
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect

# Create your views here.


def index(request):
    return render(
        request,
        'mensajeria/index.html',
    )


def browser(request):
    if request.method == 'POST':
        form = forms.BrowserForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            # ejecutamos script de scrapping
            vicidial_scrapper.search(url)

            return HttpResponse('buscando...')
    else:
        form = forms.BrowserForm()

    return render(
        request,
        'mensajeria/browser.html',
        context={
            'form': form,
        }
    )

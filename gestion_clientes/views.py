from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import request, JsonResponse, HttpResponse
from . import models, forms
from mongo.connection import get_database, get_connection
from mongo.utils.serializer import data_serializer
from mongo.shortcuts import multi_collection_search
from pymongo import errors as mongoerrors

# Create your views here.

# Creando conexion global a mongo
client = get_connection()


def index(request):

    return render(
        request,
        'gestion_clientes/index.html'
    )


def asignation_management(request):

    return render(
        request,
        'gestion_clientes/asignation_mgmnt.html'
    )


class UploadInformationView(CreateView):
    model = models.AsignationModification
    template_name = 'gestion_clientes/upload_information.html'
    form_class = forms.AsignationModificationForm
    success_url = reverse_lazy('reportes:success')


# def mongo_browser(request):
#     db = get_database('sample_analytics')
#     collection = db.get_collection('customers')
#     data = list(collection.find())
#     data = [data_serializer(doc) for doc in data]

#     return JsonResponse(data, safe=False)


def mongo_browser(request):
    if request.method == 'POST':
        form = forms.MongoSampleDataForm(request.POST)
        if form.is_valid():
            try:
                db = get_database('sample_analytics', client)
                collection_name = form.cleaned_data['collection']
                # other_collections = [
                #     collection for collection in db.list_collection_names() if collection != collection_name]

                data = []

                if collection_name:
                    no_keys = ['collection', 'csrfmiddlewaretoken']
                    collection = db.get_collection(collection_name)
                    search = {}
                    for key in request.POST.keys():
                        if any(key in llave for llave in no_keys):
                            continue
                        value = form.cleaned_data[key]
                        if value:
                            print(f'{key}: {value}')
                            search[key] = value
                    print(search)

                    data = list(collection.find(search))
                    data = [data_serializer(doc) for doc in data]

                    return JsonResponse(data, safe=False)

                else:
                    raise NameError('No se encontro la coleccion')
            except Exception as err:
                print(
                    f'Error al buscar la informacion solicitada\nError -> {err}')
            finally:
                db.client.close()
    else:
        form = forms.MongoSampleDataForm()

    return render(
        request,
        'gestion_clientes/mongo_browser.html',
        context={
            'form': form,
        }
    )

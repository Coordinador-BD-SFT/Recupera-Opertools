from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import request, JsonResponse, HttpResponse
from . import models, forms
from mongo.connection import get_database
from mongo.utils.serializer import data_serializer
from pymongo import errors as mongoerrors

# Create your views here.


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
                db = get_database('sample_analytics')
                collection_name = form.cleaned_data['collection']
                data = []

                if collection_name == 'accounts':
                    collection = db.get_collection(collection_name)
                    account_id = form.cleaned_data['account_id']
                    limit = form.cleaned_data['limit']

                    data = list(collection.find_one(
                        {'account_id': account_id}))

                elif collection_name == 'customers':
                    collection = db.get_collection(collection_name)
                elif collection_name == 'transactions':
                    collection = db.get_collection(collection_name)
                else:
                    raise NameError('No se encontro la coleccion')
            except (mongoerrors.ConnectionFailure, NameError) as err:
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

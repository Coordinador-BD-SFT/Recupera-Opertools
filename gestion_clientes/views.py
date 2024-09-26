from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import request
from . import models, forms
from utils.pyspark_.clean_base import read_file
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

    def form_valid(self, form):
        file = form.cleaned_data['file']
        print(type(file))
        print(read_file(file.name))
        return super().form_valid(form)

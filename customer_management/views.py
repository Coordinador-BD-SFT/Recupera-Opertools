from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import request
from . import models, forms
# Create your views here.


def index(request):

    return render(
        request,
        'customer_management/index.html'
    )


def asignation_management(request):

    return render(
        request,
        'customer_management/asignation_mgmnt.html'
    )


class UploadInformationView(CreateView):
    model = models.AsignationModification
    template_name = 'customer_management/upload_information.html'
    form_class = forms.AsignationModificationForm
    success_url = reverse_lazy('reportes:success')

    def form_valid(self, form):
        pass
        return super().form_valid(form)

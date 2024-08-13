from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect

# Create your views here.


def index(request):
    return HttpResponse('<h1>Bienvenido a la app de mensajeria</h1>')

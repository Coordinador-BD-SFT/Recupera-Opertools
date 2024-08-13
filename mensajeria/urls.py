from django.urls import path
from . import views

app_name = 'mensajeria'
urlpatterns = [
    path('', views.index, name='index')
]

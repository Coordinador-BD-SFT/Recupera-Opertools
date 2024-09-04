from django.urls import path
from . import views

# (Convención) Definimos variable app_name para referenciar las urls mas fácilmente
app_name = 'mensajeria'

# (Convención) Lista de funciones path que definen las URLs del proyecto
urlpatterns = [
    path('', views.index, name='index'),
    path('whatsapp_scraping', views.whatsapp_scraping, name='whatsapp_scraping'),
]

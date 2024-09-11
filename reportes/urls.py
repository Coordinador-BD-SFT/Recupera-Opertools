from django.urls import path
from . import views

"""
Modulo de definición de las URLs de la app
"""

# (convención) Definimos el nombre de la app para poder referenciar URLs más fácilmente
app_name = 'reportes'

# (Convención) Lista de funciones path que definen las URLs del proyecto
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:tipo_reporte_name>', views.reporte, name='reporte'),
    path('<str:tipo_reporte_name>/crear', views.reporte_form, name='crear'),
    path(
        '<str:tipo_reporte_name>/<int:reporte_id>',
        views.reporte_detalle,
        name='reporte_detalle'
    ),
    path(
        '<str:tipo_reporte_name>/<int:reporte_id>/download',
        views.reporte_download,
        name='reporte_download'
    ),
    path(
        '<str:tipo_reporte_name>/sms_bases',
        views.sms_bases,
        name='sms_bases'
    ),
    path(
        '<str:report_type_name>/actualizar_bases/<int:sms_base_id>',
        views.sms_base_update,
        name='sms_update'
    ),
    path(
        '<str:report_type_name>/actualizar_bases/<int:sms_base_id>/download',
        views.sms_base_download,
        name='sms_base_download'
    ),
    path('scrapers/<scraper_id>', views.scrapers, name='scrapers'),
    path('vicidial/clean_lists', views.clean_lists, name='clean_lists'),
    path('vicidial/download_lists', views.download_lists, name='download_lists'),
    path('vicidial/upload_lists', views.upload_lists, name='upload_lists'),
    path('telematica/whatsapp', views.whatsapp_scraping, name='whatsapp_scraping'),
    path('success', views.success, name='success'),
]

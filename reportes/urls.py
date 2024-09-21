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
    # Modulo reportes
    path('reportes', views.tipos_reporte, name='tipos_reporte'),
    path('reportes/<str:tipo_reporte_name>', views.reporte, name='reporte'),
    path('reportes/<str:tipo_reporte_name>/crear',
         views.reporte_form, name='crear'),
    path(
        'reportes/<str:tipo_reporte_name>/<int:reporte_id>',
        views.reporte_detalle,
        name='reporte_detalle'
    ),
    path(
        'reportes<str:tipo_reporte_name>/<int:reporte_id>/download',
        views.reporte_download,
        name='reporte_download'
    ),
    path('resources', views.resources, name='resources'),
    path('reportes/resources/listas',
         views.lists_resources, name='lists_resources'),
    path('reportes/resources/sms', views.sms_resources, name='sms_resources'),
    path('files_bases', views.files_and_bases, name='files_bases'),
    path('resources/update_lists', views.UpdateLists.as_view(), name='update_lists'),
    path(
        'resources/update_sms_files',
        views.UpdateSMSFiles.as_view(),
        name='update_sms_files'
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
    # Fin modilo reportes
    # Modulo vicidial
    path('vicidial', views.vicidial, name='vicidial'),
    path('vicidial/clean_lists', views.clean_lists, name='clean_lists'),
    path('vicidial/download_lists', views.download_lists, name='download_lists'),
    path('vicidial/upload_lists', views.upload_lists, name='upload_lists'),
    # Fin modulo vdicial
    # Modulo trelematica
    path('telematica/whatsapp', views.whatsapp_scraping, name='whatsapp_scraping'),
    # Fin modulo telematica
    path('process/success', views.success, name='success'),
]

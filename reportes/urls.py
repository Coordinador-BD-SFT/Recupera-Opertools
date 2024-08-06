from django.urls import path
from . import views


app_name = 'reportes'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:tipo_reporte_name>', views.reporte, name='reporte'),
    path('<str:tipo_reporte_name>/crear', views.reporte_form, name='crear'),
    path('<str:tipo_reporte_name>/<int:reporte_id>',
         views.reporte_detalle, name='reporte_detalle'),
    path(
        '<str:tipo_reporte_name>/actualizar_base',
        views.sms_bases,
        name='sms_bases'
    ),
    path(
        '<str:report_type_name>/actualizar_bases/<int:sms_base_id>',
        views.sms_base_update,
        name='sms_update'
    ),
    path('success', views.success, name='success'),
]

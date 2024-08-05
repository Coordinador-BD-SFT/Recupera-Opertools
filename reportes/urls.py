from django.urls import path
from . import views


app_name = 'reportes'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:tipo_reporte_name>', views.reporte, name='reporte'),
    path('<str:tipo_reporte_name>/crear', views.reporte_form, name='crear'),
    path('<str:tipo_reporte_name>/<int:reporte_id>',
         views.reporte_detalle, name='reporte_detalle'),
]

from django.urls import path
from . import views

app_name = 'customer_management'
urlpatterns = [
    path('', views.index, name='index'),
    path(
        'asignation-management',
        views.asignation_management,
        name='asignation_mgmnt'
    ),
    path(
        'asignation-management/upload-information',
        views.UploadInformationView.as_view(),
        name='upload_information'
    ),
]

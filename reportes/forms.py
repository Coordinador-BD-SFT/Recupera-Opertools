from django import forms
from .models import ReporteWhatsapp

# create your forms here


class UploadChatBaseForm(forms.ModelForm):
    class Meta:
        model = ReporteWhatsapp
        fields = ['title', 'tipo_reporte', 'chats', 'basedata']

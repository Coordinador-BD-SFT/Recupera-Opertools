from django import forms
from . import models

# create your forms here


class Reporteform(forms.ModelForm):
    class Meta:
        model = models.Reporte
        fields = ['name', 'campaign', 'chats_file',
                  'envio_sms_file', 'report_type', 'hora']
        widgets = {
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

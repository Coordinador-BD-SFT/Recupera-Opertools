from django import forms
from . import models

# create your forms here


class Reporteform(forms.ModelForm):
    VALID_EXTENSIONS = ['.csv', '.json', '.xls']

    class Meta:
        model = models.Reporte
        fields = ['name', 'campaign', 'chats_file',
                  'envio_sms_file', 'report_type', 'hora']
        widgets = {
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def clean_chats_file(self):
        chats = self.cleaned_data.get('chats_file')

        if chats:
            if not any(chats.name.endswith(ext) for ext in self.VALID_EXTENSIONS):
                raise forms.ValidationError(
                    f"Las extensiones soportadas son: {', '.join(self.VALID_EXTENSIONS)}.")
        return chats

    def clean_envio_sms_file(self):
        sms = self.cleaned_data.get('envio_sms_file')

        if sms:
            if not any(sms.name.endswith(ext) for ext in self.VALID_EXTENSIONS):
                raise forms.ValidationError(
                    f"Las extensiones soportadas son: {', '.join(self.VALID_EXTENSIONS)}.")
        return sms

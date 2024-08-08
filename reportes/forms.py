from django import forms
from . import models

# create your forms here


class Reporteform(forms.ModelForm):
    VALID_EXTENSIONS = ['.csv', '.json', '.xlsx']

    class Meta:
        model = models.Reporte
        fields = ['name', 'campaign', 'chats_file',
                  'numero_inicio', 'numero_final', 'report_type', 'hora']
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

    def clean_numero_inicio(self):
        num = self.cleaned_data.get('numero_inicio', '')
        num = [char for char in num if char != ' ']
        num = ''.join(num)
        return num

    def clean_numero_final(self):
        num = self.cleaned_data.get('numero_final')
        num = [char for char in num if char != ' ']
        num = ''.join(num)
        return num


class SMSBaseUpdateForm(forms.Form):
    nueva_base = forms.FileField(required=True, label='Nueva base de SMS')

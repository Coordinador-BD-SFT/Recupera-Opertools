from utils.dataframes import whatsapp
from django import forms
from . import models
import pandas as pd
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

# create your forms here


class Reporteform(forms.ModelForm):
    VALID_EXTENSIONS = ['.csv', '.json', '.xlsx']

    class Meta:
        model = models.Reporte
        fields = ['campaign', 'chats_file',
                  'numero_inicio', 'numero_final', 'report_type', 'hora']
        widgets = {
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('campaign', css_class='form-select', id='validationCustom01'),
            Field('chats_file', css_class='form-control',
                  id='validationCustom01'),
            Field('numero_inicio', css_class='form-control',
                  id='validationCustom01'),
            Field('numero_final', css_class='form-control',
                  id='validationCustom01'),
            Field('report_type', css_class='form-select',
                  id='validationCustom01'),
            Field('hora', css_class='form-control', id='validationCustom01'),
        )

    def clean_chats_file(self):
        chats = self.cleaned_data.get('chats_file')
        cols_needed = ['phone_number']

        if chats:
            if not (any(chats.name.endswith(ext) for ext in self.VALID_EXTENSIONS) and whatsapp.file_verify(chats, cols_needed)):
                raise forms.ValidationError(
                    f"""
                    Hubo un error al procesar el archivo, por favor revise el tipo de archivo o su contenido.
                    Las extensiones soportadas son: {', '.join(self.VALID_EXTENSIONS)}.
                    Las columnas necesarias son: {', '.join(cols_needed)}.
                    """
                )

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
    VALID_EXTENSIONS = ['.csv', '.json', '.xlsx']

    nueva_base = forms.FileField(required=True, label='Nueva base de SMS')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nueva_base', css_class='form-control',
                  id='validationCustom01')
        )

    def clean_nueva_base(self):
        base = self.cleaned_data.get('nueva_base')
        cols_needed = ['Dato_Contacto', 'Identificacion',
                       'Cuenta_Next', 'Edad_Mora']

        if base:
            if not (any(base.name.endswith(ext) for ext in self.VALID_EXTENSIONS) and whatsapp.file_verify(base, cols_needed)):
                raise forms.ValidationError(
                    f"""
                        Hubo un error al procesar el archivo, por favor revise el tipo de archivo o su contenido.
                        Las extensiones soportadas son: {', '.join(self.VALID_EXTENSIONS)}.
                        Las columnas/propiedades necesarias son: {', '.join(cols_needed)}.
                        """
                )
        return base

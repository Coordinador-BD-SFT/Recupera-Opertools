from utils.dataframes import whatsapp
from django import forms
from . import models
import pandas as pd

# Importamos modulo de renderizado de formularios con Bootstrap
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

# create your forms here


class Reporteform(forms.ModelForm):
    """
    Formulario basado en el modelo Reporte
    """

    # Deifinimos extensiones validas para el archivo de numeros de whatsapp
    VALID_EXTENSIONS = ['.csv', '.json', '.xlsx']

    class Meta:
        model = models.Reporte
        fields = ['campaign', 'chats_file',
                  'numero_inicio', 'numero_final', 'report_type', 'hora']
        widgets = {
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    # Reescribimos el constructor para poder utilizar la libreria de renderizado de formularios con Bootstrap5
    def __init__(self, *args, **kwargs):
        # Lamamos al constructor padre para crear correctamente la instancia del formulario
        super().__init__(*args, **kwargs)

        # Definimos las variables para el renderizado con Bootsrap5
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Damos clases boostrap a todos los campos del formulario
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
        # Función que maneja las validaciones del campo de chats_file en el formulario

        chats = self.cleaned_data.get('chats_file')
        cols_needed = ['phone_number']
        extension = chats.name.split('.')[-1]

        # Verificamos que el archivo cumpla con tener una de las extensiones válidas
        if chats:
            if not (any(chats.name.endswith(ext) for ext in self.VALID_EXTENSIONS) and whatsapp.file_verify(chats, cols_needed, extension)):
                # Levantamos un ValidaionError en caso de que no cumpla
                raise forms.ValidationError(
                    f"""
                    Hubo un error al procesar el archivo, por favor revise el tipo de archivo o su contenido.
                    Las extensiones soportadas son: {', '.join(self.VALID_EXTENSIONS)}.
                    Las columnas necesarias son: {', '.join(cols_needed)}.
                    """
                )
        # Retornamos el archivo
        return chats

    def clean_numero_inicio(self):
        # Función para validar el campo numero_inicio del formulario
        # Obtenemos campo y establacemos opcionalidad
        num = self.cleaned_data.get('numero_inicio', '')
        # Retornamos campo sin epacios
        return ''.join([char for char in num if char != ' '])

    def clean_numero_final(self):
        # Función para validar el campo numero_final del formulario
        # Obtenemos campo
        num = self.cleaned_data.get('numero_final')
        # Retornamos campo sin espacios
        return ''.join([char for char in num if char != ' '])


class SMSBaseUpdateForm(forms.Form):
    """
    Formulario para actualizar bases de SMS (No basado en modelo)
    """

    # Definimos extensiones válidas
    VALID_EXTENSIONS = ['.csv', '.json', '.xlsx']

    # Campo del formulario
    nueva_base = forms.FileField(required=True, label='Nueva base de SMS')

    # Reescribimos el constructor para utilizar la libreria de validacion de formularios con Bootsrap5
    def __init__(self, *args, **kwargs):
        # Llamamos al construcor padre para crear correctamente la instancia del formulario
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Asignamos clases e identificadores css al campo
            Field('nueva_base', css_class='form-control',
                  id='validationCustom01')
        )

    def clean_nueva_base(self):
        # Función para validar el campo nueva_base del forumlario

        # Obtenemos el archivo
        base = self.cleaned_data.get('nueva_base')
        cols_needed = ['Dato_Contacto', 'Identificacion',
                       'Cuenta_Next', 'Edad_Mora']
        # Verificamos que el archivo cumpla con las extensiones validas y las columnas necesarias
        if base:
            if not (any(base.name.endswith(ext) for ext in self.VALID_EXTENSIONS) and whatsapp.file_verify(base, cols_needed)):
                # En caso de no cumplir levntamos un ValidationError
                raise forms.ValidationError(
                    f"""
                        Hubo un error al procesar el archivo, por favor revise el tipo de archivo o su contenido.
                        Las extensiones soportadas son: {', '.join(self.VALID_EXTENSIONS)}.
                        Las columnas/propiedades necesarias son: {', '.join(cols_needed)}.
                        """
                )
        # Retornamos el archivo
        return base


class WhatsappScrapingForm(forms.Form):
    search_types = [
        ('num_veryfing', 'Verificar Numeros'),
        ('send_messages', 'Enviar Mensajes'),
    ]

    messages = forms.FileField(required=True, label='Mensajes')
    nums_verify = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
        label='Solo verificar números'
    )

    # Reescribimos el constructor para utilizar libreria de renderizado de formularios con Bootstrap5
    def __init__(self, *args, **kwargs):
        # Llamamos al constructor padre para crear correctamente la instancia del formulario
        super().__init__(*args, **kwargs)
        # Definimos variables para el renderizado con Bootstrap5
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Agregamos clases e identificadores Bootstrap5
            Field('messages', css_class='form-control', id='validationCustom01'),
            Field(
                'nums_verify',
                css_class='form-check-input',
                id='flexSwitchCheckReverse',
                type='checkbox'
            )
        )


class MultipleFileInput(forms.ClearableFileInput):
    """
    Agrega posibilidad de leer multiples archivos en un solo campo de formulario
    """
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    Campo para subir múltiples archivos en un solo input
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, value, initial=None):
        if isinstance(value, (list, tuple)):
            return [super(MultipleFileField, self).clean(file) for file in value if file]
        return super(MultipleFileField, self).clean(value)


class UpdateListsForm(forms.Form):
    """
    Formulario para actualizar la carpeta de donde se obtienen las listas a cargar
    """
    lists_files = MultipleFileField(label='selecciona los nuevos archivos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('lists_files', css_class='form_control',
                  id='formFileMultiple')
        )


class UpdateSMSFilesForm(forms.Form):
    sms_files = MultipleFileField(label='selecciona los nuevos archivos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('sms_files', css_class='form_control', id='formFileMultiple')
        )

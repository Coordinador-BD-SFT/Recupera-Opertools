from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout

# Create your forms here

# Formulario para el envío auomatico de whatsapp


class WhatsappScrapingForm(forms.Form):
    messages = forms.FileField(required=True, label='Mensajes')

    # Reescribimos el constructor para utilizar libreria de renderizado de formularios con Bootstrap5
    def __init__(self, *args, **kwargs):
        # Llamamos al constructor padre para crear correctamente la instancia del formulario
        super().__init__(*args, **kwargs)
        # Definimos variables para el renderizado con Bootstrap5
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Agregamos clases e identificadores Bootstrap5
            Field('messages', css_class='form-control', id='validationCustom01')
        )

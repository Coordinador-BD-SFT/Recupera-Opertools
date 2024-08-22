from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout


class WhatsappScrapingForm(forms.Form):
    messages = forms.FileField(required=True, label='Mensajes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('messages', css_class='form-control', id='validationCustom01')
        )

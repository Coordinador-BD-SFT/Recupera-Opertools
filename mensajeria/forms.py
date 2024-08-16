from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout


class BrowserForm(forms.Form):
    url = forms.URLField(max_length=200, required=True,
                         label='Recupera Browser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.layout = Layout(
            Field('url', css_class='form-control')
        )

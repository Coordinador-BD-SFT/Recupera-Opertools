from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class AsignationModificationForm(forms.ModelForm):
    class Meta:
        model = models.AsignationModification
        fields = ['name', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-select', id='validationCustom01'),
            Field('file', css_class='form-control', id='validationCustom01')
        )

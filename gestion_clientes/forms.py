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


# class MongoBrowserForm(forms.Form):
    # account = forms.IntegerField(label='N° de obligacion')
    # document = forms.CharField(max_length=200, label='N° de identificación')
    # number = forms.IntegerField(label='Numero')
    # email = forms.CharField(max_length=200, label='Correo')
    # name = forms.CharField(max_length=200, label='Nombre')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Field('account', css_class='form-control', id='validationCustom01'),
    #         Field('document', css_class='form-control', id='validationCustom01'),
    #         Field('number', css_class='form-control', id='validationCustom01'),
    #         Field('email', css_class='form-control', id='validationCustom01'),
    #         Field('name', css_class='form-control', id='validationCustom01')
    #     )


class MongoSampleDataForm(forms.Form):
    collections = [
        ('accounts', 'Cuentas'),
        ('customers', 'Clientes'),
        ('transactions', 'Transacciones')
    ]

    collection = forms.ChoiceField(choices=collections, label='Buscar por')
    account_id = forms.IntegerField(
        label='Numero de cuenta',
        required=False
    )
    limit = forms.IntegerField(
        label='Limite de cuenta',
        required=False
    )
    username = forms.CharField(
        max_length=200,
        label='Nombre/Username',
        required=False
    )
    email = forms.EmailField(
        max_length=200,
        label='Email',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('collection', css_class='form-control',
                  id='validationCustom01'),
            Field('account_number', css_class='form-control',
                  id='validationCustom01'),
            Field('account_limit', css_class='form-control',
                  id='validationCustom01'),
            Field('customer_username_name',
                  css_class='form-control', id='validationCustom01'),
            Field('customer_mail', css_class='form-control',
                  id='validationCustom01'),
        )

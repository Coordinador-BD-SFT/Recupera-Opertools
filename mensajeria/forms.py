from django import forms


class BrowserForm(forms.Form):
    url = forms.URLField(max_length=200, required=True,
                         label='Recupera Browser')

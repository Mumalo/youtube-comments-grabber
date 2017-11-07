from django import forms
from django.core.exceptions import ValidationError


class UrlForm(forms.Form):
    url = forms.URLField(required=True)

    def __init__(self, *args, **kwargs):
        super(UrlForm, self).__init__(*args, **kwargs)
        self.fields['url'].label = ''
        self.fields['url'].widget.attrs['placeholder'] = 'Enter URL'

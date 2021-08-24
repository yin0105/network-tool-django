from django import forms
from django.conf import settings

from datetime import date, datetime, timedelta
from .validators import validate_domain


class WhoisForm(forms.Form):

    whois_domain_name = forms.CharField(
                    widget=forms.TextInput(
                        attrs={ 'id': 'whois_domain_name',
                                'class': 'form-control',
                                'type': 'text', 
                                'placeholder': 'google.com',
                                'required': 'true'}
                    ),
                    label='Domain name',
                    max_length=50,
                    validators=[validate_domain],
                )
    
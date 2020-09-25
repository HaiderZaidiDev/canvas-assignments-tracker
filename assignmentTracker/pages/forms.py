from django import forms
from django.db import models
from .models import AccessToken

class AccessTokenForm(forms.ModelForm):
    class Meta:
        model = AccessToken
        fields = ['token']
        widgets = {
            'token': forms.TextInput(attrs={'placeholder': 'Access Token', 'required':True})
            }

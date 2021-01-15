from django import forms
from .models import  Web


class WebForm(forms.ModelForm):
    """Form for the web model"""

    class Meta:
        model = Web
        fields = ('ph_num', 'name')


class AuthForm(forms.Form):
    ph_num = forms.CharField(max_length=10, required=True)
    name = forms.CharField(max_length=50)


class StatusForm(forms.Form):
    ph_num = forms.CharField(max_length=10, required=True)

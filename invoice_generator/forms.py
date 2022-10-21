from django import forms
from django.forms import inlineformset_factory

from invoice_generator.models import ClientInfo, Service


class ClientInfoForms(forms.ModelForm):
    class Meta:
        model = ClientInfo
        widgets = {
            'total_amount': forms.HiddenInput()
        }
        fields = '__all__'


class ServiceForms(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ('client', 'id'),


ServiceFormset = inlineformset_factory(ClientInfo, Service, fields=['description', 'taxed', 'amount'],
                                       extra=1, can_delete=False)

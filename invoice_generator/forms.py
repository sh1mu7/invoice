from django import forms
from django.forms import inlineformset_factory

from invoice_generator.models import ClientInfo, Service


class ClientInfoForms(forms.ModelForm):
    class Meta:
        model = ClientInfo
        fields = '__all__'


class ServiceForms(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


ServiceFormset = inlineformset_factory(ClientInfo, Service, fields=('name', 'quantity', 'price'), extra=1)

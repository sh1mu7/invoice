import datetime
import os.path
import ssl
import tempfile
from fileinput import filename

from django import template
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from num2words import num2words
from weasyprint import html, HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from config.settings import BASE_DIR
from invoice_generator.forms import ClientInfoForms, ServiceFormset
from invoice_generator.models import Service, ClientInfo
from django.http import HttpResponse
import functools

from django.conf import settings
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher


# Create your views here.
def invoice_create(request):
    forms = ClientInfoForms(request.POST or None)
    formset = inlineformset_factory(ClientInfo, Service, fields=['description', 'taxed', 'amount'],
                                    extra=1,
                                    can_delete=False)
    formset = formset(request.POST or None, queryset=Service.objects.none())
    if request.method == 'POST':
        if forms.is_valid() and formset.is_valid():
            client = forms.save(commit=False)
            client.save()
            temp = 0
            for form in formset:
                service = form.save(commit=False)
                service.client = client
                temp += service.amount
                client.total_amount = temp
                service.save()
                client.save()
        return redirect('invoice:create_invoice')

    context = {
        'forms': forms,
        'formset': formset
    }
    return render(request, 'home.html', context)


def invoice_list(request):
    context = {
        'objects': ClientInfo.objects.all()
    }
    return render(request, 'invoice_list.html', context)


def invoice_edit(request, pk):
    client_id = ClientInfo.objects.get(id=pk)
    forms = ClientInfoForms(request.POST or None, instance=client_id)

    formset = inlineformset_factory(ClientInfo, Service, fields=['description', 'taxed', 'amount'],
                                    extra=0,
                                    can_delete=False)
    formset = formset(request.POST or None, instance=client_id)
    if request.method == 'POST':
        if forms.is_valid() and formset.is_valid():
            client = forms.save(commit=False)
            client.save()
            for form in formset:
                service = form.save(commit=False)
                service.client_id = client_id

                service.save()
        return redirect('invoice:invoice_list')
    context = {
        'forms': forms,
        'formset': formset
    }
    return render(request, 'invoice_edit.html', context)


def invoice_delete(request, pk):
    client_id = ClientInfo.objects.get(id=pk)
    client_id.delete()
    return redirect('invoice:invoice_list')


def invoice_details(request, pk):
    context = {
        'Objects': ClientInfo.objects.get(id=pk),
        'Services': Service.objects.filter(client_id__exact=pk),
        'subtotal': Service.objects.filter(client_id__exact=pk).aggregate(Sum('amount'))['amount__sum'],
        'subtotal_in_word': num2words(
            Service.objects.filter(client_id__exact=pk).aggregate(Sum('amount'))['amount__sum'])
    }
    return render(request, 'invoice_details.html', context)


def export_pdf(request, pk):
    context = {
        'Objects': ClientInfo.objects.get(id=pk),
        'Services': Service.objects.filter(client_id__exact=pk),
        'subtotal': Service.objects.filter(client_id__exact=pk).aggregate(Sum('amount'))['amount__sum'],
        'subtotal_in_word': num2words(
            Service.objects.filter(client_id__exact=pk).aggregate(Sum('amount'))['amount__sum'])
    }
    html_string = render_to_string('invoice.html', context)
    html = HTML(string=html_string)
    queryset = ClientInfo.objects.filter(id=pk)
    for query in queryset:
        result = os.path.join(BASE_DIR + '/media/invoice', query.invoice_no + '.pdf')
        html.write_pdf(result, stylesheets=['/home/sh1mu7/Desktop/projects/invoice/static/assets/css/style.css'])

    return render(request, 'invoice.html', context)

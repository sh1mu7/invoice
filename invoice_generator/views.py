from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

from invoice_generator.forms import ClientInfoForms, ServiceFormset
from invoice_generator.models import Service, ClientInfo


# Create your views here.
def invoice_create(request):
    forms = ClientInfoForms(request.POST or None)
    formset = inlineformset_factory(ClientInfo, Service, fields=['name', 'quantity', 'price'],
                                    extra=1,
                                    can_delete=False)
    formset = formset(request.POST or None, queryset=Service.objects.none())
    if request.method == 'POST':
        if forms.is_valid() and formset.is_valid():
            client = forms.save(commit=False)
            client.save()
            for form in formset:
                service = form.save(commit=False)
                service.client = client
                service.save()
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

    formset = inlineformset_factory(ClientInfo, Service, fields=['name', 'quantity', 'price'],
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
        'objects': ClientInfo.objects.get(id=pk),
        'service':Service.objects.filter(client_id__exact=pk)

    }
    return render(request, 'invoice_details.html', context)

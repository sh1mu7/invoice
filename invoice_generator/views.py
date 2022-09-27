from django.http import HttpResponse
from django.shortcuts import render, redirect

from invoice_generator.forms import ClientInfoForms, ServiceForms, ServiceFormset
from invoice_generator.models import Service, ClientInfo


# Create your views here.
def home(request):
    forms = ClientInfoForms(request.POST or None)
    formset = ServiceFormset(request.POST or None, queryset=Service.objects.none())
    if request.method == 'POST':
        if forms.is_valid() and formset.is_valid():
            client = forms.save(commit=False)
            client.save()
            for form in formset:
                service = form.save(commit=False)
                service.client = client
                service.save()
        return redirect('invoice:home')

    context = {
        'forms': forms,
        'formset': formset
    }
    return render(request, 'home.html', context)

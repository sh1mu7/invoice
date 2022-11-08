from django.urls import path
from .views import invoice_create, invoice_list, invoice_edit, invoice_delete, invoice_details, export_pdf
from django.conf.urls.static import static
from django.conf import settings

app_name = 'invoice'

urlpatterns = [
    path('', invoice_create, name='create_invoice'),
    path('invoice_list', invoice_list, name='invoice_list'),
    path('invoice_edit/<int:pk>', invoice_edit, name='invoice_edit'),
    path('invoice_details/<int:pk>', invoice_details, name='invoice_details'),
    path('invoice_delete/<int:pk>', invoice_delete, name='invoice_delete'),
    path('export-invoice/<int:pk>', export_pdf, name='pdf')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

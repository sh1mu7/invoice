import datetime
from random import random

from django.db import models
from django.urls import reverse


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def increment_invoice_number():
    last_invoice = ClientInfo.objects.all().order_by('id').last()
    if not last_invoice:
        return 'INV_XX_01047'
    invoice_no = last_invoice.invoice_no
    invoice_int = int(invoice_no.split('_')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'INV_XX_0' + str(new_invoice_int)
    return new_invoice_no


class ClientInfo(BaseModel):
    # STATUS_CHOICES = (
    #     ('Paid', 'Paid'),
    #     ('Overdue', 'Overdue'),
    #     ('Cancelled', 'Cancelled')
    # )
    name = models.CharField(max_length=200, verbose_name="Client's Name", null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    invoice_no = models.CharField(max_length=500, editable=False,
                                  default=increment_invoice_number, null=True, blank=True)

    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False)

    class Meta:
        db_table = 'Client_Information'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("client_details", args=[str(self.id)])


class Service(BaseModel):
    name = models.CharField(max_length=300, verbose_name='Service Name', null=False, blank=False)
    quantity = models.CharField(max_length=5, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    client = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='client_name')

    class Meta:
        db_table = 'Service'

    def __str__(self):
        return self.name

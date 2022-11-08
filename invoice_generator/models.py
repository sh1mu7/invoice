from django.db import models
from django.db.models import signals
from django.dispatch import receiver
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
        return 'INV_01047'
    invoice_no = last_invoice.invoice_no
    invoice_int = int(invoice_no.split('_')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'INV_0' + str(new_invoice_int)
    return new_invoice_no


class ClientInfo(BaseModel):
    name = models.CharField(max_length=200, verbose_name="Name", null=False, blank=False)
    org_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    tax_amount = models.IntegerField(null=True, blank=True)
    vat_amount = models.IntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0)
    address = models.CharField(max_length=500, blank=False, null=False)
    invoice_no = models.CharField(max_length=500, editable=False,
                                  default=increment_invoice_number, null=True, blank=True)

    class Meta:
        db_table = 'Client_Information'

    @property
    def vat_calculate(self):
        if self.vat_amount is None:
            return 0
        else:
            vat_payment = (self.total_amount * self.vat_amount) / 100
            vat_applied = self.total_amount + (self.total_amount * self.vat_amount) / 100
            return vat_payment, vat_applied

    @property
    def tax_calculate(self):
        if self.tax_amount is None:
            return self.total_amount
        else:
            tax_applied = self.total_amount - (self.total_amount * self.tax_amount) / 100
            tds = (self.total_amount * self.tax_amount) / 100
            return tds, tax_applied


    def get_absolute_url(self):
        return reverse("client_details", args=[str(self.id)])

    def __str__(self):
        return self.name


class Service(BaseModel):
    description = models.CharField(max_length=300, verbose_name='Description', null=False, blank=False)
    taxed = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='client_name')

    class Meta:
        db_table = 'Service'

    def __str__(self):
        return self.description


@receiver(signals.post_save, sender=Service)
def create_service(sender, instance, created, **kwargs):
    print(ClientInfo.pk)

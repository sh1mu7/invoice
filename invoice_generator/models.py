from django.db import models
from django.urls import reverse


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ClientInfo(BaseModel):
    name = models.CharField(max_length=200, verbose_name="Client's Name", null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)

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

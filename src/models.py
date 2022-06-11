from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=250)
    telephone_number = models.IntegerField(blank=True, null=True)
    mobile_number = models.IntegerField(blank=True, null=True)
    with_contract = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.FloatField(max_length=20, blank=True, null=True)
    signed = models.BooleanField(default=False)
    date_signed = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.client.last_name


class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True)
    date_of_event = models.DateTimeField(blank=True, null=True)
    last_day_of_event = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StatusContract(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='sales_contact')
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='support_contact')

    def __str__(self):
        return str(self.contract)

# Create your models here.

from django.db import models
from authentication.models import User


class Client(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=250)
    telephone_number = models.IntegerField(blank=True, null=True)
    mobile_number = models.IntegerField(blank=True, null=True)
    with_contract = models.BooleanField(default=False)

    def __str__(self):
        return self.user.last_name


class Event(models.Model):
    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_of_event = models.DateTimeField(blank=True, null=True)
    last_day_of_event = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_contact')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_contact')
    signed = models.BooleanField(default=False)
    date_signed = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    """def __str__(self):
        return self.client.last_name"""

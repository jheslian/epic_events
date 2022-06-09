from django.contrib import admin
from .models import  Client, Contract, Event


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'sales_contact', 'with_contract')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('client', 'signed')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'support_contact', 'date_of_event')


admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)

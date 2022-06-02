from django.contrib import admin
from .models import User, Client, Contract, Event


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'last_name')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('client', 'with_contract')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('client', 'sales_contact')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'date_of_event')


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)

from django.contrib.auth.models import Group

from .models import Client, Contract, Event
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'company_name', 'telephone_number', 'mobile_number',
                  'with_contract']


class ContractSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Contract
        fields = ['id', 'client', 'amount', 'signed', 'date_signed', 'expiry_date', 'date_created']

    def to_representation(self, instance):
        self.fields['client'] = ClientSerializer(read_only=True)
        return super().to_representation(instance)


class EventSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'location', 'description', 'contract', 'support_contact', 'date_of_event',
                  'last_day_of_event', 'date_created']

    def to_representation(self, instance):
        user_group = Group.objects.get(user=self.context.get('request').user)
        if str(user_group) != 'support':
            self.fields['contract'] = ContractSerializer(read_only=True)
        return super().to_representation(instance)

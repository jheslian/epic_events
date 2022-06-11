from collections import OrderedDict
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Client, Contract, Event, StatusContract
from rest_framework import generics
from rest_framework.response import Response
from .permissions import ContractPermission, ClientsPermission, EventsPermission
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from datetime import datetime
from django.db.models import Q


class ClientView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientsPermission]
    filterset_fields = ['last_name', 'email']

    def get_queryset(self):
        """ Query the clients that are only related to the current user.
        If user is manager this will return all the data """
        contract_status = StatusContract.objects.filter(
            Q(sales_contact=self.request.user) | Q(support_contact=self.request.user))
        user_group = Group.objects.get(user=self.request.user)
        clients_id = []
        if str(user_group.name) == 'sales' or str(user_group.name) == 'support':
            for obj in contract_status:
                clients_id.append(obj.contract.client.id)
            return self.queryset.filter(id__in=clients_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': 'Client created.', 'data': request.data}, status=201)


class ClientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientsPermission]
    lookup_url_kwarg = 'client_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': "Client updated", 'data': serializer.data})


class ContractView(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermission]
    filterset_fields = {
        'client__last_name': ['exact', 'contains'],
        'client__email': ['exact'],
        'signed': ['exact'],
        'amount': ['exact', 'gt'],
        'date_created': ['gte', 'lte'],
    }

    def get_queryset(self):

        """ Query the contracts that are only related to the current user.
        If user is manager this will return all the data """
        contract_status = StatusContract.objects.filter(
            Q(sales_contact=self.request.user) | Q(support_contact=self.request.user))
        user_group = Group.objects.get(user=self.request.user)
        contracts_id = []
        if str(user_group.name) == 'sales' or str(user_group.name) == 'support':
            for obj in contract_status:
                contracts_id.append(obj.contract.id)
            return self.queryset.filter(id__in=contracts_id)
        return self.queryset

    def perform_create(self, serializer):
        obj = serializer.save()
        StatusContract.objects.create(contract=obj)
        return serializer

    def create(self, request, *args, **kwargs):
        """ Customize contract
             - Add manually the client to the contract
             - date_signed is automatically added when a contract is signed
        """
        data = OrderedDict()
        data.update(request.data)
        try:
            client = get_object_or_404(Client, email=data['client'])
            data['client'] = client.id
            if data['signed'] == 'true':
                data['date_signed'] = datetime.now()
        except Exception as e:
            print(e)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({'message': 'Contract created.', 'data': serializer.data},
                        status=201, headers=headers)


class ContractDetailView(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermission]
    lookup_url_kwarg = 'contract_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': "Contract updated", 'data': serializer.data})


class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, ContractPermission]
    filterset_fields = {
        'contract__client__last_name': ['exact'],
        'contract__client__email': ['exact'],
        'date_created': ['gte', 'lte'],
    }

    def get_queryset(self):

        """ Filters the events that are only related to the current user.
        If user is manager this will return all the data """
        try:
            contract_status = StatusContract.objects.filter(
                Q(sales_contact=self.request.user) | Q(support_contact=self.request.user))
            user_group = Group.objects.get(user=self.request.user)
            events_id = []
            if str(user_group.name) == 'sales' or str(user_group.name) == 'support':
                for obj in contract_status:
                    events_id.append(obj.contract.id)
                return self.queryset.filter(id__in=events_id)
        except Exception as e:
            print(e)
        return self.queryset

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': 'Event created.', 'data': request.data}, status=201)


class EventDetailView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventsPermission]
    lookup_url_kwarg = 'event_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': "Event updated", 'data': serializer.data})

from collections import OrderedDict

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import User, Client, Contract, Event
from rest_framework import generics
from rest_framework.response import Response
from .permissions import IsInSalesOrManagement, IsInSupportOrManagement
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from datetime import datetime


class ClientView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsInSalesOrManagement]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['last_name', 'email']

    def perform_create(self, serializer):
        sales_contact = get_object_or_404(User, id=self.request.user.id)
        return serializer.save(sales_contact=sales_contact)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': 'Client created.', 'data': request.data}, status=201)


class ClientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsInSalesOrManagement]
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
    permission_classes = [IsAuthenticated, IsInSalesOrManagement]
    filterset_fields = {
        'client__last_name': ['exact', 'contains'],
        'client__email': ['exact'],
        'signed': ['exact'],
        'amount': ['exact', 'gt'],
        'date_created': ['gte', 'lte'],
    }

    def create(self, request, *args, **kwargs):
        """ Customise contract
             - Add manually the client to the contract
             - date_signed is automatically added when a contract is signed
        """
        data = OrderedDict()
        data.update(request.data)
        try:
            client = get_object_or_404(Client, email=data['client'])
            data['client'] = client.id
            if data['signed'] is 'true':
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
    permission_classes = [IsAuthenticated, IsInSalesOrManagement]
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
    permission_classes = [IsAuthenticated, IsInSupportOrManagement]
    filterset_fields = {
        'contract__client__last_name': ['exact'],
        'contract__client__email': ['exact'],
        'date_created': ['gte', 'lte'],
    }

    def create(self, request, *args, **kwargs):
        data = OrderedDict()
        data.update(request.data)
        try:
            user = get_object_or_404(User, username=data['support_contact'])
            data['support_contact'] = user.id
        except Exception as e:
            print(e)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({'message': 'Contract created.', 'data': serializer.data},
                        status=201, headers=headers)


class EventDetailView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsInSupportOrManagement]
    lookup_url_kwarg = 'event_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': "Event updated", 'data': serializer.data})

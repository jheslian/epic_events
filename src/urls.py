from django.urls import path
from .views import ClientView, ClientDetailView, ContractView, ContractDetailView, EventView, EventDetailView

urlpatterns = [
    path('clients', ClientView.as_view()),
    path('clients/<int:client_id>', ClientDetailView.as_view(), name='client-name'),
    path('contracts', ContractView.as_view()),
    path('contracts/<int:contract_id>', ContractDetailView.as_view()),
    path('events', EventView.as_view()),
    path('events/<int:event_id>', EventDetailView.as_view())
]

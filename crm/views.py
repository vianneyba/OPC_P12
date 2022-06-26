from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from crm import serializers, models, permissions
from authenticate.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response

class ClientViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.ClientPermissions,)
    serializer_class = serializers.ClientSerializer



    def get_queryset(self):
        queryset = models.Client.objects.all()
        if self.request.query_params.get('name') is not None:
            name = self.request.query_params.get('name')
            queryset = queryset.filter(last_name__icontains=name)
        if self.request.query_params.get('email') is not None:
            email = self.request.query_params.get('email')
            queryset = queryset.filter(email__icontains=email)
        if self.request.query_params.get('customer') is not None:
            customer = self.request.query_params.get('customer')
            queryset = queryset.filter(prospect=customer)
        if self.request.query_params.get('vendor') is not None:
            vendor = self.request.query_params.get('vendor')
            queryset = queryset.filter(sales_contact__pk=vendor)

        return queryset

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data["sales_contact"] = request.user.pk
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None):
        request.data._mutable = True
        request.data["sales_contact"] = request.user.pk
        request.data._mutable = False
        return super().update(request, pk)


class ContractViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.ContractPermissions,)

    def get_queryset(self):
        queryset = models.Contract.objects.all()

        if self.request.query_params.get('client_id') is not None:
            client = self.request.query_params.get('client_id')
            queryset = queryset.filter(client__pk=client)
        if self.request.query_params.get('client') is not None:
            name = self.request.query_params.get('client')
            queryset = queryset.filter(client__last_name__icontains=name)
        if self.request.query_params.get('company') is not None:
            company = self.request.query_params.get('company')
            queryset = queryset.filter(client__company__icontains=company)
        if self.request.query_params.get('email') is not None:
            email = self.request.query_params.get('email')
            queryset = queryset.filter(client__email__icontains=email)
        if self.request.query_params.get('date') is not None:
            date = self.request.query_params.get('date')
            if date[0] == '>':
                queryset = queryset.filter(date_created__gt=date[1:])
            elif date[0] == '<':
                queryset = queryset.filter(date_created__lte=date[1:])
            else:
                queryset = queryset.filter(date_created=date)
        if self.request.query_params.get('amount') is not None:
            amount = self.request.query_params.get('amount')
            if amount[0] == '>':
                queryset = queryset.filter(amount__gt=amount[1:])
            elif amount[0] == '<':
                queryset = queryset.filter(amount__lte=amount[1:])
            else:
                queryset = queryset.filter(amount=amount)

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return serializers.ContractAddSerializer
        else:
            return serializers.ContractSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data["sales_contact"] = request.user.pk
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None):
        request.data._mutable = True
        request.data["sales_contact"] = request.user.pk
        request.data._mutable = False
        return super().update(request, pk)


class EventViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.EventPermission,)

    def get_queryset(self):
        queryset = models.Event.objects.all()

        if self.request.query_params.get('email') is not None:
            email = self.request.query_params.get('email')
            queryset = queryset.filter(client__email__icontains=email)
        if self.request.query_params.get('client_id') is not None:
            client = self.request.query_params.get('client_id')
            print(client)
            queryset = queryset.filter(client__pk=client)
        if self.request.query_params.get('client') is not None:
            name = self.request.query_params.get('client')
            queryset = queryset.filter(client__last_name__icontains=name)
        if self.request.query_params.get('date') is not None:
            date = self.request.query_params.get('date')
            if date[0] == '>':
                queryset = queryset.filter(event_date__date__gt=date[1:])
            elif date[0] == '<':
                queryset = queryset.filter(event_date__date__lte=date[1:])
            else:
                queryset = queryset.filter(event_date=date)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.EventAddSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.EventUpdateSerializer
        else:
            return serializers.EventSerializer
        
    def create(self, request, *args, **kwargs):
        contract = models.Contract.objects.get(pk=request.data["contract"])
        request.data._mutable = True
        request.data["client"] = contract.client.pk
        request.data["sales_contact"] = request.user.pk
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None):
        contract = models.Contract.objects.get(pk=request.data["contract"])
        request.data._mutable = True
        request.data["client"] = contract.client.pk
        request.data["sales_contact"] = request.user.pk
        request.data._mutable = False
        return super().update(request, pk)

class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, permissions.UserPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
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
    queryset = models.Event.objects.all()

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
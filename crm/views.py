from django.shortcuts import render
from rest_framework import viewsets
from crm import serializers, models

class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()


class ContractViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ContractSerializer
    queryset = models.Contract.objects.all()


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
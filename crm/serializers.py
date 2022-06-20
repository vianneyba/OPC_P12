from rest_framework import serializers
from crm import models


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):

    client = ClientSerializer()

    class Meta:
        model = models.Contract
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):

    client = ClientSerializer()
    
    class Meta:
        model = models.Event
        fields = '__all__'

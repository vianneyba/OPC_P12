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


class ContractAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Contract
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    client = ClientSerializer()
    contract = ContractSerializer()
    
    class Meta:
        model = models.Event
        fields = '__all__'

class EventAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = '__all__'

class EventUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = models.Event
        fields = ('event_status', 'attendees', 'event_date', 'notes', 'contract')

    def save(self, **kwargs):
        print(kwargs)
        for r in self.validated_data:
            print(r)

        return super().save(**kwargs)
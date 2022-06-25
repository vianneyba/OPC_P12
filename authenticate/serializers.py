from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name',
            'last_name', 'email', 'password',
            'groups', 'is_staff'
        ]
        extra_kwargs = {
            'password': {'write_only': True}}

    def create(self, data):
        user = User.objects.create_user(data['username'],
            email=data['email'], password=data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.groups.set(data['groups'])
        user.is_staff = data["is_staff"]
        user.save()
        return user

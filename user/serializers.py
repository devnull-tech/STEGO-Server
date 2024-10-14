from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_pgp_public_key')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email')

    def create(self, data) -> CustomUser:
        user = CustomUser.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return user
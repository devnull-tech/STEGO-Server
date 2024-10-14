from rest_framework import serializers
from django.urls import reverse
from .models import Container
from user.models import CustomUser as User

class ContainerDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    b64_photo = serializers.CharField()

    class Meta:
        model = Container
        fields = ('id', 'user', 'b64_photo')


class ContainerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    container_url = serializers.SerializerMethodField()
    b64_photo = serializers.CharField(write_only=True)
    
    class Meta:
        model = Container
        fields = ('id', 'user', 'b64_photo', 'container_url')

    def create(self, validated_data) -> Container:
        new_container = Container.objects.create(
            user = validated_data['user'],
            b64_photo = validated_data['b64_photo']
        )
        return new_container
    
    def get_container_url(self, obj):
        return reverse('get_container', kwargs={'container_id': obj.pk})
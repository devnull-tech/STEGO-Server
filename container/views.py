from . import models
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import ContainerSerializer, ContainerDetailSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_container(request):
    data = {
        'user': request.user.id,
        'b64_photo': models.Container.get_base_photo()
    }
    serializer = ContainerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_container_list(request):
    user = request.user
    containers = models.Container.objects.filter(user=user)
    serializer = ContainerSerializer(containers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_container(request, container_id):
    user = request.user
    try:
        container = models.Container.objects.get(user=user, id=container_id)
    except models.Container.DoesNotExist:
        return Response({"error": "Container not found"}, status=404)
    serializer = ContainerDetailSerializer(container, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def inupt(request, container_id):
    user = request.user
    try:
        container = models.Container.objects.get(user=user, id=container_id)
        if not request.data.get('text'):
            return Response({"error": "'text' field not provided"}, status=status.HTTP_400_BAD_REQUEST)
        container.input(request.data.get('text'))
        return redirect('get_container', container_id=container_id)
    except models.Container.DoesNotExist:
        return Response({"error": "Container not found"}, status=404)
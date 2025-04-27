from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Pereval
from .serializers import PerevalSerializer, PerevalUpdateSerializer
from tourist.models import Tourist
from coordinates.models import Coords
from photo.models import Image


class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PerevalUpdateSerializer
        return PerevalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'Перевал успешно создан',
                'id': serializer.instance.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 400,
            'message': 'Ошибка в данных запроса',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверяем статус перевала, можно редактировать только со статусом "new"
        if instance.status != 'new':
            return Response({
                'state': 0,
                'message': f'Невозможно редактировать перевал со статусом {instance.get_status_display()}'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'state': 1,
                'message': 'Перевал успешно обновлен'
            })
        return Response({
            'state': 0,
            'message': 'Ошибка в данных запроса',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def user_submitted(self, request):
        email = request.query_params.get('user__email', None)
        if email:
            perevals = Pereval.objects.filter(tourist__email=email)
            serializer = PerevalSerializer(perevals, many=True)
            return Response(serializer.data)
        return Response({'message': 'Email параметр не указан'}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render

# Create your views here.

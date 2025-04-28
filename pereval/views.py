from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, RedirectView
from .models import Pereval, TermsAgreement
from .serializers import (
    PerevalSerializer,
    PerevalUpdateSerializer,
    PerevalDetailSerializer,
    PerevalListSerializer
)
from tourist.models import Tourist
from coordinates.models import Coords
from photo.models import Image
import uuid
from django.conf import settings


class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PerevalUpdateSerializer
        return PerevalSerializer

    def create(self, request, *args, **kwargs):
        # Проверяем наличие токена согласия с условиями
        terms_token = request.data.get('terms_token')
        if not terms_token:
            return Response({
                'status': 400,
                'message': 'Отсутствует подтверждение согласия с условиями обработки персональных данных',
                'id': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем действительность токена
        try:
            terms_agreement = TermsAgreement.objects.get(token=terms_token)
            if not terms_agreement.is_valid:
                return Response({
                    'status': 400,
                    'message': 'Токен согласия недействителен или истек',
                    'id': None
                }, status=status.HTTP_400_BAD_REQUEST)
        except TermsAgreement.DoesNotExist:
            return Response({
                'status': 400,
                'message': 'Токен согласия не найден',
                'id': None
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Помечаем токен как использованный
            terms_agreement.is_valid = False
            terms_agreement.save()

            return Response({
                'status': 200,
                'message': 'Перевал успешно создан',
                'id': serializer.instance.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 400,
            'message': 'Ошибка в данных запроса',
            'errors': serializer.errors,
            'id': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверяем статус перевала, можно редактировать только со статусом "new"
        if instance.status != 'new':
            return Response({
                'state': 0,
                'message': f'Невозможно редактировать перевал со статусом {instance.get_status_display()}',
                'id': instance.id
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'state': 1,
                'message': 'Перевал успешно обновлен',
                'id': instance.id
            })
        return Response({
            'state': 0,
            'message': 'Ошибка в данных запроса',
            'errors': serializer.errors,
            'id': instance.id
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def user_submitted(self, request):
        email = request.query_params.get('user__email', None)
        if email:
            perevals = Pereval.objects.filter(tourist__email=email)
            serializer = PerevalSerializer(perevals, many=True)
            return Response(serializer.data)
        return Response({'message': 'Email параметр не указан'}, status=status.HTTP_400_BAD_REQUEST)


class PerevalDetailView(generics.RetrieveAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalDetailSerializer


class UserPerevalListView(generics.ListAPIView):
    serializer_class = PerevalListSerializer

    def get_queryset(self):
        email = self.request.query_params.get('user__email', None)
        if email:
            return Pereval.objects.filter(tourist__email=email)
        return Pereval.objects.none()


class TermsAgreementView(TemplateView):
    template_name = 'terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем return_url из параметров запроса или используем значение по умолчанию
        return_url = self.request.GET.get('return_url', settings.DEFAULT_RETURN_URL)

        # Генерируем уникальный токен
        token = str(uuid.uuid4())

        # Сохраняем токен в базе данных
        TermsAgreement.objects.create(token=token, is_valid=True)

        context['return_url'] = return_url
        context['token'] = token
        return context


class TermsRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return_url = self.request.GET.get('return_url', '/')
        token = self.request.GET.get('token', '')

        # Формируем URL для редиректа с токеном
        if '?' in return_url:
            return f"{return_url}&terms_token={token}"
        else:
            return f"{return_url}?terms_token={token}"
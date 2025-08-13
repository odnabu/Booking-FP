# apps/addresses/views.py
# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError


from apps.addresses.models import *
from apps.addresses.serializers import *
from common.permissions import IsLandlordOrAdminOrReadOnly


# NB!  ModelViewSet - для каждой модели используется ЕДИНОЖДЫ.

class AddressViewSet(viewsets.ModelViewSet):
    """
    This view provides a complete set of CRUD actions for the Address model.
    API endpoint that allows addresses to be VIEWED or EDITED.
    Get a list of addresses for ADMIN.
    """
    queryset = Address.objects.all()

    # Настройка фильтрации для модели Address:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['street', 'city', 'country']
    # Поля, по которым будет работать полнотекстовый поиск (search=...):
    search_fields = ['street', 'city', 'country']
    # Поля, по которым можно будет сортировать (ordering=...):
    ordering_fields = ['id', 'country', 'city', 'street']

    # Явно указываем классы разрешений для этого представления:
    permission_classes = [IsLandlordOrAdminOrReadOnly]

    # _____  Переопределяем метод ViewSet  ______
    # Этот метод позволяет динамически выбирать сериалайзер для метода GET:
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких, как GET:
        if self.action == 'list':
            return ListAddressSerializer
        # Для остальных методов (POST, PUT, DELETE):
        return AddressSerializer

    # Этот метод переопределяет perform_create, чтобы при создании нового адреса запретить дублирование по всем полям:
    # Смотри здесь подсказки: https://chatgpt.com/s/t_6894513b8f08819181931849ac3449dd
    def perform_create(self, serializer):
        data = serializer.validated_data

        if Address.objects.filter(
                apartment_number=data.get('apartment_number'),
                building=data.get('building'),
                street=data.get('street'),
                province=data.get('province'),
                city=data.get('city'),
                country=data.get('country'),
                zip_code=data.get('zip_code')
        ).exists():
            raise ValidationError("This address already exists.")

        serializer.save()

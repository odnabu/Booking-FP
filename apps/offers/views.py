from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action


from apps.offers.models import *
from apps.offers.serializers import *
from apps.offers.models import Offer
from common.permissions import IsLandlordOrAdminOrReadOnly


# NB!  ModelViewSet - для каждой модели используется ЕДИНОЖДЫ.


# Кастомный фильтр-класс для фильтрации с диапазоном из DjangoFilterBackend: RangeFilter или NumberFilter
# с аргументами lookup_expr='gte' и lookup_expr='lte'.
# Отправлять GET-запросы вида: /api/v1/offers/?price_min=500&price_max=1000.
# https://chatgpt.com/s/t_68952953508c8191bb8bfedbf5d6173d
class OfferFilter(FilterSet):
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')
    rooms_min = NumberFilter(field_name='rooms', lookup_expr='gte')
    rooms_max = NumberFilter(field_name='rooms', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = [
            'price_min', 'price_max',
            'rooms_min', 'rooms_max',
            'address__city',
            'real_estate_type',
        ]


class OfferViewSet(viewsets.ModelViewSet):
    """
    Offer to rent out real estate.
    For Landlords and Admins allows you to filter, search, or order.
    """
    queryset = Offer.objects.all()

    # Настройка фильтрации для модели Offer:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Поля, по которым можно будет точно фильтровать (price=...):
    # filterset_fields = ['price', 'address__country',
    #                     'real_estate_type', 'rooms']
    filterset_class = OfferFilter
    # Поля, по которым будет работать полнотекстовый поиск (search=...):
    search_fields = ['title', 'description']
    # Поля, по которым можно будет сортировать (ordering=...):
    ordering_fields = ['price', 'updated_at']

    # Явно указываем классы разрешений для этого представления:
    permission_classes = [IsLandlordOrAdminOrReadOnly]  # только пользователям с ролью арендодателя "landlord"
                                                        # или Админам могут создавать, обновлять и удалять предложения.

    # _____  Переопределяем метод ViewSet  ______
    # Метод позволяет динамически выбирать сериалайзер:
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких, как GET:
        if self.action == 'list':
            return ListOfferSerializer
        # Для остальных методов (POST, PUT, DELETE):
        return OfferSerializer

    # Метод позволяет только пользователям с ролью арендодателя "Landlord" или Админам создавать предложения:
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Метод позволяет арендаторам или незарегистрированным пользователям видеть
    # только активные предложения https://chatgpt.com/s/t_6895171fb8e481919dcce1b3e1ec12e2:
    def get_queryset(self):
        user = self.request.user

        # Если пользователь не аутентифицирован или арендатор:
        if not user.is_authenticated or getattr(user.profile, 'role', None) == 'tenant':
            return Offer.objects.filter(is_active=True)

        # Если админ или арендодатель — возвращаем все
        return Offer.objects.all()

    # Переключение статуса is_active, чтобы арендодатель мог скрыть или открыть своё объявление.
    # При этом отправлять POST-запрос на /api/v1/offers/<id>/toggle_active/, чтобы временно скрыть или сделать
    # активным объявление.
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_active(self, request, pk=None):
        offer = self.get_object()

        # Только владелец или админ может переключать статус
        if offer.user != request.user and not request.user.is_staff:
            return Response({'detail': 'You do not have permission to do this.'},
                            status=status.HTTP_403_FORBIDDEN)

        offer.is_active = not offer.is_active
        offer.save()
        return Response({'is_active': offer.is_active}, status=status.HTTP_200_OK)




from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.reviews.models import *
from apps.reviews.serializers import *
from apps.reviews.models import Review
# from common.permissions import IsOwnerOrReadOnly


# NB!  ModelViewSet - для каждой модели используется ЕДИНОЖДЫ.

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Reviews of real estate from tenants.
    """
    queryset = Review.objects.all()

    # Настройка фильтрации для модели Review:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Поля, по которым можно будет точно фильтровать (username=...):
    filterset_fields = ['rating', 'reviewer__username', 'booking__offer__address']
    # Поля, по которым будет работать полнотекстовый поиск (search=...):
    search_fields = ['rating', 'reviewer__username', 'booking__offer__address']
    # Поля, по которым можно будет сортировать (ordering=...):
    ordering_fields = ['created_at']

    # Явно указываем классы разрешений для этого представления:
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsLandlordOrAdminOrReadOnly]  # только пользователям с ролью арендодателя "landlord"

    # _____  Переопределяем метод ViewSet  ______

    # Этот метод позволяет динамически выбирать сериалайзер:
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких, как GET:
        if self.action == 'list':
            return ListReviewSerializer
        # Для остальных методов (POST, PUT, DELETE):
        return ReviewSerializer

    # CRUD, но без возможности менять отзыв чужого пользователя.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    # Эндпоинт для отзывов по конкретному предложению:
    # GET /reviews/offer/{offer_id}/ — отзывы для конкретного объявления.
    @action(detail=False, methods=['get'], url_path='offer/(?P<offer_id>[^/.]+)')
    def reviews_for_offer(self, request, offer_id=None):
        """
        Reviews for a specific offer.
        """
        reviews = Review.objects.filter(booking__offer__id=offer_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

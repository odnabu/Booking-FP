from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta


from apps.bookings.models import *
from apps.bookings.serializers import *
# from common.permissions import IsTenantOrAdminOrReadOnly


# NB!  ModelViewSet - для каждой модели используется ЕДИНОЖДЫ.

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to make or editing bookings.
    For Landlords and Admins allows you to filter, search, or order.
    """
    queryset = Booking.objects.all()

    # Настройка фильтрации для модели Booking:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['start_date', 'status', 'offer__address']
    # Поля, по которым будет работать полнотекстовый поиск (search=...):
    search_fields = ['start_date', 'status', 'offer__owner__username']
    # Поля, по которым можно будет сортировать (ordering=...):
    ordering_fields = ['created_at']

    # Явно указываем классы разрешений для этого представления:
    # permission_classes = [IsTenantOrAdminOrReadOnly]    # только пользователям с ролью арендатора "tenant",
    #                                                     # или Админам могут создавать, обновлять и удалять бронирования.
    permission_classes = [IsAuthenticated]          # ВСЕ аутентифицированные пользователи могу бронировать.

    # _____  Переопределяем метод ViewSet  ______
    # Этот метод позволяет динамически выбирать сериалайзер:
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких, как GET:
        if self.action in ['list', 'all_bookings']:     # Разеление для админов и остальных пользователей.
            return ListBookingSerializer
        # Для остальных методов (POST, PUT, DELETE):
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user,)

    # Переопределение метода get_queryset, чтобы админы могли переходить по специальному для них эндпоинту
    # для просмотра всего списка бронирований.
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Booking.objects.all()                # админ видит всё
    #     return Booking.objects.filter(tenant=user)      # остальные — только свои
    def get_queryset(self):
        """
        For a regular /bookings/ endpoint, we return only the current user's bookings,
        regardless of whether he is an admin or not.
        """
        return Booking.objects.filter(tenant=self.request.user)


    @action(detail=False, methods=['get'],
            permission_classes=[IsAdminUser],
            url_path='all')
    def all_bookings(self, request):
        """
        Additional endpoint for admins: viewing all bookings with filtering, searching and sorting.
        """
        qs = self.filter_queryset(Booking.objects.all())
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    # Просмотр бронирований (свои активные и завершённые).
    # Фильтрация queryset в get_queryset, чтобы пользователь видел только свои бронирования (как tenant или landlord).
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Active bookings
        """
        bookings = self.get_queryset().filter(end_date__gte=now().date())
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Completed bookings.
        """
        bookings = self.get_queryset().filter(end_date__lt=now().date())
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


    # Отмена бронирования (только до определённой даты)
    # Запрет отмены, если до начала бронирования осталось меньше 2 дней.
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancellation of booking (only 2 days before the start).
        """
        booking = self.get_object()

        if booking.tenant != request.user:
            return Response({"error": "You cannot cancel this reservation."}, status=403)

        if booking.start_date - now().date() < timedelta(days=2):
            return Response({"error": "Cancellation is possible no later than 2 days before the start."}, status=400)

        booking.status = 'cancelled'
        booking.save()
        return Response({"status": "Reservation cancelled."})


    # Подтверждение / отклонение бронирования (для арендодателя)
    # Для booking.landlord (он же booking.offer.owner):
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Booking confirmation (landlord only).
        """
        booking = self.get_object()

        if booking.landlord != request.user:
            return Response({"error": "You are not the owner of the property.."}, status=403)

        booking.status = 'confirmed'
        booking.save()
        return Response({"status": "Booking confirmed."})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject booking (landlord only).
        """
        booking = self.get_object()

        if booking.landlord != request.user:
            return Response({"error": "You are not the owner of the property."}, status=403)

        booking.status = 'cancelled'
        booking.save()
        return Response({"status": "Reservation rejected."})


# apps/bookings/views.py
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

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


    # _____  ПЕРЕОПРЕДЕЛЕНИЯ  метода  ViewSet  ___________________________________________________________

    # Этот метод позволяет динамически выбирать сериалайзер:
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких, как GET:
        if self.action in ['list', 'landlord_bookings']:     # Разделение для landlords и остальных пользователей.
            return ListBookingSerializer
        # Для остальных методов (POST, PUT, DELETE):
        return BookingSerializer

    # Переопределение метода get_queryset, чтобы админы, как пользователи с тремя ролями (admain,
    # tenant, landlord) могли переходить по специальному для них эндпоинту
    # для просмотра разных списков списка бронирований.
    # 2-nd Variant
    # def get_queryset(self):
    #     """
    #     For a regular /bookings/ endpoint, we return only the current user's bookings,
    #     regardless of whether he is an admin or not.
    #     """
    #     return Booking.objects.filter(tenant=self.request.user)
    # 3-d Variant:
    def get_queryset(self):
        user = self.request.user
        # для списка — арендаторы видят только свои брони:
        if self.action == 'list':
            return Booking.objects.filter(tenant=user)
        # для retrieve (детали) — либо мои (админа) как арендатора, либо на мою недвижимость:
        if self.action in ['retrieve', 'confirm_booking', 'reject_booking']:
            return Booking.objects.filter(tenant=user) | Booking.objects.filter(offer__owner=user)
        if user.is_staff and self.action == 'all_bookings':
            return Booking.objects.all()            # админ видит всё
        return Booking.objects.none()

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user,)


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


    # Отмена бронирования съемщиком (Tenant): только до определённой даты.
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
    # Как это работает:
    #   - Арендатор → видит свои брони по /bookings/ и может сделать бронирование.
    #   - Лендлорд → видит список бронирований на свои объекты по /bookings/landlord/.
    #   - Лендлорд → может подтвердить или отменить бронирование через /bookings/{id}/confirm/ или /bookings/{id}/cancel/.
    #   - Админ → может делать всё.

    # Список бронирований других пользователей на объекты, которыми владеет текущий пользователь:
    @action(detail=False, methods=['get'], url_path='landlord')
    def landlord_bookings(self, request):
        """
        List of reservations for properties owned by the current user (if they have the landlord role).
        """
        user = request.user
        if user.profile.role != 'landlord' and not request.user.is_staff:
            return Response({"detail": "Not allowed. You have no permissions to this action."}, status=403)
        bookings = Booking.objects.filter(offer__owner=user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    # Подтверждение бронирования (только для владельца или админа):
    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm_booking(self, request, pk=None):
        """
        Booking confirmation (for owner or admin only).
        """
        booking = self.get_object()
        if booking.offer.owner != request.user and not request.user.is_staff:
            return Response({"detail": "Not allowed. You have no permissions to this action."}, status=status.HTTP_403_FORBIDDEN)
        booking.status = 'confirmed'
        booking.save()
        return Response({"status": "Booking confirmed."})

    # Отмена бронирования (только для владельца или админа):
    @action(detail=True, methods=['post'], url_path='reject')
    def reject_booking(self, request, pk=None):
        """
        Reject a booking (for owner or admin only).
        """
        booking = self.get_object()
        if booking.offer.owner != request.user and not request.user.is_staff:
            return Response({"detail": "Not allowed. You have no permissions to this action."},
                            status=status.HTTP_403_FORBIDDEN)
        booking.status = 'canceled'
        booking.save()
        return Response({"status": "Booking rejected."})

    # Админ видит бронирования: и свои на не свою недвижимость и других пользователей на свою:
    @action(detail=False, methods=['get'], url_path='all')
    def all_bookings(self, request):
        """
        The admin sees reservations: both his own for someone else's property and other users' for his own.
        """
        user = request.user
        if user.profile.role != 'landlord' and not request.user.is_staff:
            return Response({"detail": "Not allowed. You have no permissions to this action."}, status=403)
        bookings = Booking.objects.filter(tenant=user) | Booking.objects.filter(offer__owner=user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


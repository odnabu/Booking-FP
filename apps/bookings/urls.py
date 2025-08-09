# apps/bookings/urls.py
# Представления и маршруты для модели Booking.

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.bookings.views import BookingViewSet


# Создаем экземпляр роутера:
router = DefaultRouter()

# Регистрируем ViewSet.
#   BookingViewSet - представление, которое будет обрабатывать запросы.
router.register('', BookingViewSet)

# Основной список маршрутов приложения users.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
]

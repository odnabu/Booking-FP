# apps/addresses/urls.py
# Представления и маршруты для модели Address.

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.addresses.views import AddressViewSet


# Создаем экземпляр роутера:
router = DefaultRouter()

# Регистрируем ViewSet.
#   AddressViewSet - представление, которое будет обрабатывать запросы.
router.register('', AddressViewSet)

# Основной список маршрутов приложения users.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
]

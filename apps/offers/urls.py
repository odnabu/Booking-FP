# apps/offers/urls.py
# Представления и маршруты для модели Offers.

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.offers.views import OfferViewSet


# Создаем экземпляр роутера:
router = DefaultRouter()

# Регистрируем ViewSet.
#   OfferViewSet - представление, которое будет обрабатывать запросы.
router.register('', OfferViewSet)

# Основной список маршрутов приложения users.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
]


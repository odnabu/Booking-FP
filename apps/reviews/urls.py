# apps/reviews/urls.py
# Представления и маршруты для модели Review.

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.reviews.views import ReviewViewSet


# Создаем экземпляр роутера:
router = DefaultRouter()

# Регистрируем ViewSet.
#   ReviewViewSet - представление, которое будет обрабатывать запросы.
router.register('', ReviewViewSet)

# Основной список маршрутов приложения users.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
]

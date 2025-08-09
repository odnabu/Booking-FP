# apps/users/urls.py
# Представления и маршруты для моделей User и UserProfile.

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.users.views import RegistrationView, LoginView, LogoutView, UserViewSet


# Создаем экземпляр роутера:
router = DefaultRouter()

# Регистрируем ViewSet.
#   UserViewSet - представление, которое будет обрабатывать запросы.
router.register('', UserViewSet)

# Основной список маршрутов приложения users.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
    # path('registration/', RegistrationView.as_view(), name='booking-registration'),
    # path('login/', LoginView.as_view(), name='booking-login'),
    # path('logout/', LogoutView.as_view(), name='booking-logout'),
]


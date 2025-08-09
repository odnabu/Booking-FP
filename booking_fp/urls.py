# booking_fp/urls.py
"""
URL configuration for booking_fp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Настройка TokenAuthentication:
from rest_framework.authtoken.views import obtain_auth_token
# JWT-аутентификация, Basic Authentication:
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import RegistrationView, LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.routers')),       # # <-- только API. api/v1/ - Лучше оставить для масштабирования системы в будущем.
    path('api/v1/registration/', RegistrationView.as_view(), name='booking-registration'),  # <-- HTML форма регистрации
    path('api/v1/login/', LoginView.as_view(), name='booking-login'),
    path('api/v1/logout/', LogoutView.as_view(), name='booking-logout'),
]


# _____ Настройка TokenAuthentication - аутентификация с использованием токенов:
urlpatterns += [
    # Маршрут для получения токена:
    path('get-token/', obtain_auth_token, name='get_token'),
    # Маршрут для получения access и refresh токенов:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Маршрут для обновления access токена с помощью refresh токена:
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# _____ Подключение Swagger и ReDoc:
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns += [
    # Схема и документация:
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


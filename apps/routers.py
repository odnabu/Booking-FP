# apps/routers.py
# Отображение классов в списке эндпоинтов.

from django.urls import path, include


urlpatterns = [
    # Получение СОКРАЩЕННОГО списка всех юзеров и создание нового юзера, причем
    # 'users' - это префикс URL, по которому будут доступны пользователи (арендодатели и съемщики):
    path('users/', include('apps.users.urls')),
    # Получение списка адресов и создание нового адреса:
    path('addresses/', include('apps.addresses.urls')),
    # Получение списка объявлений и создание нового объявления:
    path('offers/', include('apps.offers.urls')),
    # Получение списка бронирований и создание новой брони:
    path('bookings/', include('apps.bookings.urls')),
    # Получение списка отзывов и создание нового отзыва:
    path('reviews/', include('apps.reviews.urls')),
]


# --------------------------------------------------------
# Для тестирования работы приложения - вывод домашней страницы с приветствием:
from apps.views import hello_user

urlpatterns += [
    path('home/', hello_user, name='home'),
]
# --------------------------------------------------------

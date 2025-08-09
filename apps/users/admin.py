# РЕГИСТРИРУЕМ модель UserProfile из models.py для отображения в Админке:
from django.contrib import admin
from django.contrib.auth.models import User

from apps.users.models import UserProfile


# Красивый класс Администратора для модели UserProfile:
class UserProfileAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели:
    list_display = ('role',)
    # Задание полей по которым будет производиться поиск:
    search_fields = ('role',)
    # Задание полей по которым будет производиться фильтрация:
    list_filter = ('role',)


admin.site.register(UserProfile)

# РЕГИСТРИРУЕМ модель Review из models.py для отображения в Админке:
from django.contrib import admin

from apps.reviews.models import Review
from  apps.bookings.models import Booking


# Красивый класс Администратора для модели Review:
class ReviewAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели:
    list_display = ('booking', 'rating', 'comment', 'reviewer')
    readonly_fields = ('created_at',)
    # Задание полей по которым будет производиться поиск:
    search_fields = ('booking', 'rating', 'reviewer')
    # Задание полей по которым будет производиться фильтрация:
    list_filter = ('rating', 'created_at')


admin.site.register(Review, ReviewAdmin)

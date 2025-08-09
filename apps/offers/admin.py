# РЕГИСТРИРУЕМ модель Offer из models.py для отображения в Админке:
from django.contrib import admin
from apps.offers.models import Offer


# Красивый класс Администратора для модели Offer:
class OfferAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели:
    list_display = ('title', 'description', 'rooms', 'real_estate_type', 'price', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    # Задание полей по которым будет производиться поиск:
    search_fields = ('title', 'description', 'price')
    # Задание полей по которым будет производиться фильтрация:
    list_filter = ('is_active',)


admin.site.register(Offer, OfferAdmin)

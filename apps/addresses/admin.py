# РЕГИСТРИРУЕМ модель Address из models.py для отображения в Админке:
from django.contrib import admin
from apps.addresses.models import Address

# Красивый класс Администратора для модели Address:
class AddressAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели:
    list_display = ['apartment_number', 'building', 'street', 'city', 'country', 'zip_code']
    # Задание полей по которым будет производиться поиск:
    search_fields = ['building', 'street', 'city', 'country']
    # Задание полей по которым будет производиться фильтрация:
    list_filter = ['building', 'street', 'city']


admin.site.register(Address, AddressAdmin)

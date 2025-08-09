# РЕГИСТРИРУЕМ модель Booking из models.py для отображения в Админке:
from django.contrib import admin
from apps.bookings.models import Booking


# Красивый класс Администратора для модели Booking:
class BookingAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели:
    list_display = ('offer', 'tenant', 'start_date', 'end_date', 'status', 'landlord')
    readonly_field = ('created_at', 'updated_at')
    # Задание полей по которым будет производиться поиск:
    search_fields = ['status', 'start_date', 'end_date']
    # Задание полей по которым будет производиться фильтрация:
    list_filter = ('status', 'start_date')



admin.site.register(Booking, BookingAdmin)

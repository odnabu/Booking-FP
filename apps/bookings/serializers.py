# -------------------------------------------------
# Сериалайзеры для модели Booking.
# -------------------------------------------------
from rest_framework import serializers
from datetime import date

from apps.bookings.models import Booking
# from apps.users.serializers import ListUserSerializer


# Получение СОКРАЩЕННОГО списка ВСЕХ бронирований:
class ListBookingSerializer(serializers.ModelSerializer):
    tenant_username = serializers.CharField(source='tenant.username', read_only=True)
    landlord_username = serializers.CharField(source='offer.owner.username', read_only=True)
    user_role = serializers.CharField(source='tenant.profile.role', read_only=True)
    offer_id = serializers.IntegerField(source='offer.id', read_only=True)
    offer_title = serializers.CharField(source='offer.title', read_only=True)
    address_id = serializers.IntegerField(source='offer.address.id', read_only=True)
    address_country = serializers.CharField(source='offer.address.country', read_only=True)
    address_city = serializers.CharField(source='offer.address.city', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user_role', 'status',
                  'offer_id', 'offer_title',
                  'tenant_username', 'landlord_username',
                  'address_id', 'address_country', 'address_city',
                  'start_date', 'end_date']   #


# Создание / обновление (Create, Update) предложения и получение ДЕТАЛЬНОЙ (Detail) информации о предложении:
class BookingSerializer(serializers.ModelSerializer):
    landlord = serializers.CharField(source='landlord.username', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['tenant']  # tenant возьмём из request

    def validate(self, data):
        # Проверка, что даты в правильном порядке:
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("The start date must be before the end date.")

        # Проверка, что дата начала не в прошлом:
        if data['start_date'] < date.today():
            raise serializers.ValidationError("Cannot book in the past.")

        # Проверка на пересечение бронирований:
        offer = data['offer']
        overlapping = Booking.objects.filter(
            offer=offer,
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date']
        ).exists()

        if overlapping:
            raise serializers.ValidationError("This accommodation is already booked for the selected dates.")

        # Запрещаем бронирование своего же жилья:
        request = self.context.get('request')
        if request and offer.owner == request.user:
            raise serializers.ValidationError("You cannot book your own property.")

        return data

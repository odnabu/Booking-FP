# -------------------------------------------------
# Сериалайзеры для модели Review.
# -------------------------------------------------
from typing import ReadOnly

from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from datetime import date
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.reviews.models import Review


# Получение сокращенного списка ВСЕХ отзывов (Reviews):
class ListReviewSerializer(serializers.ModelSerializer):
    tenant_username = ReadOnlyField(source='reviewer.username', read_only=True)
    user_role = ReadOnlyField(source='reviewer.profile.role', read_only=True)
    offer_id = serializers.CharField(source='booking.offer.id', read_only=True)
    offer_title = serializers.CharField(source='booking.offer.title', read_only=True)

    class Meta:
        model = Review
        # fields = '__all__'
        fields = ['id', 'rating', 'comment', 'tenant_username', 'user_role', 'offer_id', 'offer_title']
        read_only_fields = ['tenant_username', 'created_at']


# Получение ДЕТАЛЬНОЙ информации об отзыве, создание / обновление отзыва:
class ReviewSerializer(serializers.ModelSerializer):
    offer_id = serializers.CharField(source='booking.offer.id', read_only=True)
    offer_title = serializers.CharField(source='booking.offer.title', read_only=True)

    # POST /reviews/ — создать отзыв (только арендатор /и только после окончания бронирования/ - позже).
    # GET /reviews/ — список всех отзывов (админ видит все, пользователь — только свои).

    class Meta:
        model = Review
        fields = '__all__'

    # Проверка пользователя:
    def validate(self, data):
        booking = data['booking']
        user = self.context['request'].user
        # Пользователь должен быть арендатором этого жилья:
        if booking.tenant != user:
            raise serializers.ValidationError("You can only leave a review for your own bookings.")

        # Проверяем, что бронирование завершено
        # if booking.end_date >= date.today():
        #     raise serializers.ValidationError("It is not possible to leave a review until the booking is completed.")

        return data


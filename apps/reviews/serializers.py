# -------------------------------------------------
# Сериалайзеры для модели Review.
# -------------------------------------------------
from rest_framework import serializers

from apps.reviews.models import Review


# Получение сокращенного списка ВСЕХ отзывов (Reviews):
class ListReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = '__all__'
        fields = ['reviewer__username', 'rating', 'comment', 'booking__country']


# Получение ДЕТАЛЬНОЙ информации об отзыве, создание / обновление отзыва:
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

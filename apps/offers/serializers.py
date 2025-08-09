# -------------------------------------------------
# Сериалайзеры для модели Offer.
# -------------------------------------------------
from rest_framework import serializers

from apps.offers.models import Offer


# Получение сокращенного списка ВСЕХ предложений (Offers):
class ListOfferSerializer(serializers.ModelSerializer):
    address_id = serializers.IntegerField(source='address.id', read_only=True)
    address_country = serializers.CharField(source='address.country', read_only=True)
    address_city = serializers.CharField(source='address.city', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'real_estate_type', 'address_id', 'address_country', 'address_city',
                  'price', 'owner_username', 'is_active', 'created_at']


# Получение ДЕТАЛЬНОЙ информации о предложении, создание / обновление предложение:
class OfferSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(source='offer.id', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    address_country = serializers.CharField(source='address.country', read_only=True)
    address_city = serializers.CharField(source='address.city', read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'
        # fields = ['id', 'title', 'real_estate_type', 'address_id', 'address_country', 'address_city',]
        read_only_fields = ['owner']

    # Запрет на возможность иметь больше одного активного объявления на один и тот же адрес:
    def validate(self, data):
        address = data.get('address')
        owner = self.context['request'].user

        # Проверка: есть ли уже активное объявление по этому адресу у этого владельца
        if Offer.objects.filter(address=address, owner=owner, is_active=True).exists():
            raise serializers.ValidationError(
                "You already have an active listing for this address."
            )

        return data


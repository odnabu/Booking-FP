# -------------------------------------------------
# Сериалайзеры для модели Address.
# -------------------------------------------------
from rest_framework import serializers

from apps.addresses.models import Address


# Получение СОКРАЩЕННОГО списка ВСЕХ адресов:
class ListAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'building', 'street', 'city', 'country', 'zip_code']


# Создание / обновление (Create, Update) адреса и получение ДЕТАЛЬНОЙ (Detail) информации об адресе:
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = '__all__'
        fields = ['id', 'apartment_number', 'building', 'street', 'city', 'province', 'country', 'zip_code']

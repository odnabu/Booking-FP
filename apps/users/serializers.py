# apps/users/serializers.py

# -------------------------------------------------
# Сериалайзеры для моделей User и UserProfile.
# -------------------------------------------------
from rest_framework import serializers
from django.contrib.auth.models import User

from apps.users.models import UserProfile


# Извлечение данных из профиля: роль и номер телефона.
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # fields = ('id', 'role', 'phone_number')
        fields = '__all__'


# Получение сокращенного списка ВСЕХ пользователей: арендодателей и съемщиков.
class ListUserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(read_only=True)       # Так с комбинацией filterset_fields = ['profile__role']
    # во views.py вылетает ошибка, которую можно устранить так:
    #   1. либо Удалить profile = UserProfileSeria..., если используешь только role по source.
    #   2. либо вложить profile целиком в fields = ['username', 'profile', 'email'].
    # Мне м+больше нравится сокращенная версия по методу 1.
    role = serializers.CharField(source='profile.role', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email']       # 'profile',


# Извлечение ДЕТАЛЬНОЙ информации о пользователе из встроенной в Django модели User и профиля пользователя
# (вместе с его ролью и телефоном).
class DetailUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'first_name', 'last_name', 'email']
        read_only_fields = ['date_joined']


# Создание / обновление пользователя:
class CreateUpdateUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'



# ---------------------------------------------------------------
# Регистрация пользователя с JWT:
class UserRegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

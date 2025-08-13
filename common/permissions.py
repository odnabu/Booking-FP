# common/permissions.py
# Кастомные классы разрешений.
from rest_framework.permissions import BasePermission, SAFE_METHODS


# Для добавления нового адреса:
# https://chatgpt.com/s/t_68960241a5508191bccb6a19b7303f75
#    Разрешает доступ:
#    - всем пользователям только на чтение (GET, HEAD, OPTIONS).
#    - авторизованным Landlords — на запись и редактирование.
#    - или если пользователь админ - полный доступ.
# Для создания объявления - только пользователь с ролью "арендодатель" может создавать объявления.
# https://chatgpt.com/s/t_68950f1f51e48191a7a5e65ecd859470
class IsLandlordOrAdminOrReadOnly(BasePermission):
    """
    Allows access only to Landlords and admins for unsafe methods (POST, PUT, PATCH, DELETE).
    Viewing is open to everyone.
    """
    def has_permission(self, request, view):
        # Разрешения на чтение (GET, HEAD, OPTIONS) даем всем.
        # SAFE_METHODS — это кортеж, содержащий ('GET', 'HEAD', 'OPTIONS').
        if request.method in SAFE_METHODS:
            return True

        # Разрешение на запись (POST, PUT, PATCH, DELETE) даем только владельцу объекта.
        user = request.user
        return user.is_authenticated and (
            user.is_staff or
            hasattr(user, 'profile') and user.profile.role == 'landlord'
        )

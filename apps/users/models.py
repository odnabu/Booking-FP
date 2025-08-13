# apps/users/models.py
from django.db import models
# Подключение встроенного пользователя Django (User):
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extending Django's default (built-in) user model "User" with a related "UserProfile" model.
    """

    ROLE_CHOICES = [
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
        # ('admin', 'Admin'),
    ]

    # Additional parameters to standard Django-model User:
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null= False, blank=False, verbose_name='Role: Tenant or Landlord')
    phone_number = models.CharField(max_length=20, unique=True, null= False, blank=False)

    # Relations to other models.
    # user: ForeignKey к User. При удалении проекта пользователи (profiles) удаляются (CASCADE).
    # related_name='profiles' позволит обращаться к пользователям в других моделях через profiles_instance.profiles.all()
    user = models.OneToOneField(User,
                                # on_delete=models.PROTECT - значит, НЕЛЬЗЯ удалить профиль, если на нее уже подвязан пользователь.
                                on_delete=models.CASCADE, # Удаление профиля удаляет связанного с ним пользователя из auth_user.
                                related_name='profile'
                            )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"

    class Meta:
        ordering = ['role', 'user__last_name', 'user__first_name']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

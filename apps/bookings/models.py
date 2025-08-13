# apps/bookings/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# from django.core.exceptions import ValidationError

from apps.offers.models import Offer


# Смотри доработанный мой вариант у Чата: https://chatgpt.com/s/t_6895a812027c81919728a9889cfa4d02.
class Booking(models.Model):
    """
    Model of booking an apartment.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),         # 'Ожидает подтверждения'
        ('confirmed', 'Confirmed'),     # 'Подтверждено'
        ('cancelled', 'Cancelled'),     # 'Отменено'
    ]

    start_date = models.DateField(verbose_name="Start date")
    end_date = models.DateField(verbose_name="End date")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # ForeignKey Relations:

    # 1. Relation to User (tenant)
    # Один User может иметь МНОГО Booking как арендатор
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_bookings',  # user.tenant_bookings.all() - все бронирования как арендатор
        verbose_name='Tenant'
    )

    # 2. Relation to Offer (real_estate/property)
    # Одно Offer может иметь МНОГО Booking
    offer = models.ForeignKey(
        Offer,                          # Ссылка на модель из другого приложения
        on_delete=models.CASCADE,       # При удалении Offer удаляются все связанные Booking
        related_name='bookings',        # offer.bookings.all() - все бронирования этого объявления
        verbose_name='Offer of Real estate'
    )

    def __str__(self):
        return f"Booking #{self.id} by {self.tenant} for {self.offer.title}. Landlord is {self.offer.owner}."

    @property
    def landlord(self):
        """
        We automatically take the owner from the proposal.
        """
        return self.offer.owner

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

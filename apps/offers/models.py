# apps/offers/models.py
from django.db import models
from rest_framework.authtoken.admin import User

from apps.addresses.models import Address


class Offer(models.Model):
    """
    Offer to rent out Real estate (for booking).
    """

    title = models.CharField(max_length=150, help_text='Enter a short title of your offer.')   # Заголовок, например: "Сдаю дом с 3 спальнями и террасой в Potsdam".
    description = models.TextField(null=True, blank=True)
    rooms = models.IntegerField(verbose_name='Number of rooms')
    real_estate_type = models.CharField(max_length=150, verbose_name='Type of Real estate.',
                                        help_text='Apartment, House, Studio, Hotel, Hostel, B&Bs, etc.')   # Apartment, House, Studio, Hotel, Hostel, B&Bs & More - Bed and breakfast, B&B (с англ. — «Кровать и завтрак») — вид мини-гостиницы, типа пансион, etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True, verbose_name='Is offer active?')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # ForeignKey Relations:

    # 1. Relation to User (owner of an offer - landlord)
    # Один User может иметь МНОГО Offer
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,       # При удалении User удаляются все его Offer
        related_name='offers',          # owner.offers.all() - все объявления пользователя
        verbose_name='Owner of an offer - Landlord'
    )

    # 2. Relation to Address (the address of Real estate)
    # Один Address может использоваться в МНОГИХ Offer (например, разные квартиры в одном доме)
    address = models.ForeignKey(
        Address,        # Ссылка на модель из другого приложения
        on_delete=models.PROTECT,       # Нельзя удалить Address, если на него ссылаются Offer
        related_name='offers',          # address.offers.all() - все объявления по этому адресу
        verbose_name='Address'
    )

    def __str__(self):
        return f"Offer #{self.id}: {self.title}, Price: {self.price} €"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'


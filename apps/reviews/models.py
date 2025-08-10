# apps/reviews/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.admin import User

from apps.bookings.models import Booking


class Review(models.Model):
    """
    Reviews from users (tenants) about real estate.
    """

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 verbose_name='Rating between 1 and 5',
                                 help_text='1 - very bad, 5 - excellent.')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    # ForeignKey Relations:

    # 1. Relation to User (reviews' author)
    # Один User может написать МНОГО Review
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',         # user.reviews.all() - все отзывы пользователя
        verbose_name='Reviewer'
    )

    # 2. Связь с Booking (бронирование, по которому оставлен отзыв)
    # Одно Booking может иметь ОДИН Review (но мы используем ForeignKey для гибкости)
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='reviews',         # booking.reviews.all() - отзывы по бронированию
        verbose_name='Booking'
    )

    def __str__(self):
        return f"Review by {self.reviewer.username} - {self.rating}★"

    class Meta:
        # Ограничение: один отзыв на одно бронирование от одного пользователя
        unique_together = ['reviewer', 'booking']
        ordering = ['-created_at']



# apps/addresses/models.py
from django.db import models


class Address(models.Model):
    """
    Addresses of all users: tenants and landlords (properties' owners).
    """

    apartment_number = models.CharField(max_length=10, null=True, blank=True)
    building = models.CharField(max_length=10, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    province = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    zip_code = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return (f"{self.building}, {self.street} Str.\n "
                f"{self.city}, {self.country}\n"
                f"Zip Code: {self.zip_code}")

    class Meta:
        verbose_name_plural = 'Addresses'

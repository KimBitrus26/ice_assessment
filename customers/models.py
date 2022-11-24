from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model

from .utils import Helper

User = settings.AUTH_USER_MODEL


class Customer(models.Model):
    """model to represent Customers"""

    slug = models.SlugField(editable=False)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_slug(self):

        slug = slugify(self.name)
        if Customer.objects.filter(slug=slug).exists():
            slug = slug + "-" + str(get_user_model().objects.make_random_password(length=5,
                                    allowed_chars="01234567889"))
            if Customer.objects.filter(slug=slug).exists():
                return self.get_slug()
        return slug

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = self.get_slug()
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Model to represent Payment."""

    slug = models.SlugField(editable=False)
    reference = models.CharField(max_length=30, unique=True, default=Helper.reference_generator)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} payment"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.reference)
        super().save(*args, **kwargs)

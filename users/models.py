from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("warehouse", "Warehouse Manager"),
        ("sales", "Salesperson"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="sales")

    def __str__(self):
        return self.username

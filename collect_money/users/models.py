from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    middle_name = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        verbose_name="Middle Name",
    )
    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "middle_name",
        "last_name",
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

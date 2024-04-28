from django.db import models

from collects.models import Collect
from users.models import User


class Payment(models.Model):
    """Модель Платеж."""

    amount = models.IntegerField(
        verbose_name="Сумма",
        null=False,
    )
    date = models.DateTimeField(
        verbose_name="Дата и время",
        null=False,
    )
    collect = models.ForeignKey(
        Collect,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Сбор",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="payments",
        null=False,
        verbose_name="Плательщик",
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платёж от {self.date.date()}"

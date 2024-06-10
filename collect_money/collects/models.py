from django.db import models
from users.models import User


CAUSES = {
    "wed": "Свадьба",
    "brth": "День рождения",
    "meet": "Встреча",
    "gift": "Подарок",
    "med": "Лечение",
    "serv": "Услуги",
    "msc": "Разное",
}


class Collect(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="collects",
        null=False,
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=100, null=False, verbose_name="Название"
    )
    cause = models.CharField(
        max_length=5,
        choices=CAUSES,
        verbose_name="Повод",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    goal_amount = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Целевая сумма",
    )
    current_amount = models.IntegerField(
        default=0,
        verbose_name="Текущая сумма",
    )
    bakers_count = models.IntegerField(
        default=0,
        verbose_name="Количество участников",
    )
    image = models.ImageField(
        upload_to="collects/images/",
        null=True,
        blank=True,
        verbose_name="Обложка",
    )
    close_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Окончание сбора",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Сбор"
        verbose_name_plural = "Сборы"

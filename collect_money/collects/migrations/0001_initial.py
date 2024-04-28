# Generated by Django 5.0.4 on 2024-04-28 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Collect",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Название"),
                ),
                (
                    "cause",
                    models.CharField(
                        choices=[
                            ("wed", "Свадьба"),
                            ("brth", "День рождения"),
                            ("meet", "Встреча"),
                            ("gift", "Подарок"),
                            ("med", "Лечение"),
                            ("serv", "Услуги"),
                            ("msc", "Разное"),
                        ],
                        max_length=5,
                        verbose_name="Повод",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "goal_amount",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Целевая сумма"
                    ),
                ),
                (
                    "current_amount",
                    models.IntegerField(
                        default=0, verbose_name="Текущая сумма"
                    ),
                ),
                (
                    "bakers_count",
                    models.IntegerField(
                        default=0, verbose_name="Количество участников"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="collects/images/",
                        verbose_name="Обложка",
                    ),
                ),
                (
                    "close_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Окончание сбора"
                    ),
                ),
            ],
            options={
                "verbose_name": "Сбор",
                "verbose_name_plural": "Сборы",
                "ordering": ["-id"],
            },
        ),
    ]
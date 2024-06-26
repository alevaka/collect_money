# Generated by Django 5.0.4 on 2024-04-28 19:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("collects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="collect",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="collects",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
    ]

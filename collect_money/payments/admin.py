from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class CollectsAdmin(admin.ModelAdmin):
    """Представление модели Сбора в административной панели"""

    list_display = [
        "id",
        "collect",
        "amount",
        "user",
        "date",
    ]
    list_filter = [
        "collect",
        "user",
        "date",
    ]

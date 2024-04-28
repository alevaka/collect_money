from django.contrib import admin

from collects.models import Collect
from payments.models import Payment


class PaymentInstanceInline(admin.TabularInline):
    model = Payment

    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Collect)
class CollectsAdmin(admin.ModelAdmin):
    """Представление модели Сбора в административной панели"""

    list_display = [
        "id",
        "name",
        "cause",
        "goal_amount",
        "close_date",
        "author",
        "current_amount",
        "bakers_count",
    ]
    inlines = [PaymentInstanceInline]
    list_display_links = (
        "id",
        "name",
    )
    list_filter = [
        "cause",
        "close_date",
        "author",
    ]
    search_fields = ("name",)
    search_help_text = "Поиск по имени"

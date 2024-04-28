from django.contrib import admin

from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Отображение данных модели User в интерфейсе администратора."""

    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
    )
    list_display_links = (
        "id",
        "email",
        "username",
    )
    search_fields = (
        "id",
        "email",
        "username",
        "last_name",
    )
    search_help_text = "Поиск по имени, фамилии и e-mail."

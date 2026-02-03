from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class DefaultUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "username",
        "email",
        'bio',
        "role",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "username",
        "email",
    )
    ordering = ("id",)
    readonly_fields = ("confirmation_code",)
    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('bio', 'role')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('bio', 'role')
        }),
    )

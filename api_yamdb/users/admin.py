from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'username',
        'email',
    )
    ordering = ('id',)
    readonly_fields = ('confirmation_code',)
    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )




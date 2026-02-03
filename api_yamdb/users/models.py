from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.constants import (
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    ROLE_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
)


class User(AbstractUser):
    """Кастомная модель юзера."""

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    ROLE_CHOISES = ((ADMIN, "admin"), (MODERATOR, "moderator"), (USER, "user"))
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name="Ник пользователя",
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH, unique=True, verbose_name="Email"
    )
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH, blank=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH, blank=True, verbose_name="Фамилия"
    )
    role = models.CharField(
        "Роль",
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOISES,
        default=USER,
    )
    bio = models.TextField("Биография", blank=True)

    class Meta:
        ordering = [
            "username",
        ]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

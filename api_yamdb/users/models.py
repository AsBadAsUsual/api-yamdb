from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель юзера."""

    ADMIN = 'Admin'
    MODERATOR = 'Moderator'
    USER = 'User'

    ROLE_CHOISES = (
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User')
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOISES,
        default=USER,
    )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('username', 'email')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

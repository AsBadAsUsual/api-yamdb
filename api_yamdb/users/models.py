from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    role = models.CharField('Роль', max_length=30, blank=True)
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


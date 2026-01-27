from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    role = models.CharField('Роль', max_length=30)
    bio = models.TextField('Биография')
    confirmation_code = models.CharField(
        unique=True,
        max_length=255
    )

    class Meta:
        unique_together = ('username', 'email')

    def __str__(self):
        return self.username


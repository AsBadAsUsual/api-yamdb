from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Кастомная модель юзера."""

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    ROLE_CHOISES = ((ADMIN, "admin"), (MODERATOR, "moderator"), (USER, "user"))
    username = models.CharField(max_length=150,
                                unique=True, verbose_name='Ник пользователя')
    email = models.EmailField(max_length=254,
                              unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150,
                                  blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                 blank=True, verbose_name='Фамилия')
    role = models.CharField(
        "Роль",
        max_length=20,
        choices=ROLE_CHOISES,
        default=USER,
    )
    bio = models.TextField("Биография", blank=True)
    confirmation_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['username',]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


@receiver(post_save, sender=User)
def set_confirmation_code(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(instance)
        User.objects.filter(pk=instance.pk).update(
            confirmation_code=confirmation_code
        )
        instance.confirmation_code = confirmation_code

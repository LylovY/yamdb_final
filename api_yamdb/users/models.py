from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Ник пользователя',
        db_index=True,
    )
    email = models.EmailField(
        unique=True, max_length=254, verbose_name='email'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    code = models.CharField(max_length=40, blank=True, default=0)
    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
    )

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Делаем email обязательным и уникальным
    email = models.EmailField(
        'email address',
        unique=True,
        max_length=254,
    )
    # Ваше кастомное поле для кода подтверждения
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=50,
        blank=True,
        null=True
    )
    # Можно добавить роль (например, для прав доступа)
    bio = models.TextField('о себе', blank=True)

    # Указываем, что email теперь используется для логина вместо username (если нужно)
    # USERNAME_FIELD = 'email' 
    # REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = [
    ('admin', 'Admin role'),
    ('user', 'User role'),
    ('moderator', 'Moderator role'),
]


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='user',
    )
    token = models.CharField(
        blank=True,
        null=True,
        max_length=150,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return self.username

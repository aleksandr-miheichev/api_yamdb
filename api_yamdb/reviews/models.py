from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('anonimus', 'anonimus'),
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
        ('superuser', 'superuser'),
    ]
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, null=True)
    second_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(_('email address'), unique=True)
    conformation_code = models.BigIntegerField(null=True)
    role = models.CharField(
        max_length=200,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.CharField(max_length=200, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='email_user_unique',
                fields=['email', 'username'],
            ),
        ]

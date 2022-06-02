from authentication.manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    ROLE_CHOICES = (
        ('sales', 'Sales'),
        ('support', 'Support'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, blank=True, null=True)

    class Meta:
        permissions = (
            ("add_client", "can add client"),
            ("update_client", "can update client"),
            ("create_event", "can create event"),
            ("update_event", "can update event"),
            ("create_contract", "can create contract"),
        )

    def __str__(self):
        return self.last_name

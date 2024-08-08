from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .role import Role

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15)
    verification_code = models.CharField(max_length=6, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='customuser'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def save(self, *args, **kwargs):
        if not self.is_staff and self.role is not None:
            raise ValueError("Non-staff users cannot have a role assigned.")
        super().save(*args, **kwargs)


    @property
    def is_admin(self):
        return self.is_staff and self.role is not None
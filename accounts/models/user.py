from typing import ClassVar

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.managers.user import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model where email is the unique identifier"""

    email = models.EmailField(unique=True, db_index=True)

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(  # type: ignore[assignment]
        "auth.Group",
        related_name="accounts_users",
        blank=True,
    )
    user_permissions = models.ManyToManyField(  # type: ignore[assignment]
        "auth.Permission",
        related_name="accounts_users",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        """String representation of the user"""

        return str(self.email)

    def get_full_name(self):
        """Returns the full name of the user"""

        full_name = f"{self.first_name} "

        if self.middle_name:
            full_name += f"{self.middle_name} "

        full_name += f"{self.last_name}"
        return full_name.strip()

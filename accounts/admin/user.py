"""Admin configuration for the custom User model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):  # type: ignore[misc]
    """Admin interface for the custom User model"""

    model = User  # type: ignore[assignment]

    readonly_fields = ("last_login",)

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "middle_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name")

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    filter_horizontal = ("groups", "user_permissions")

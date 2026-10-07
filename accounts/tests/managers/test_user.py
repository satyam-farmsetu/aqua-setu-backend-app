from django.test import TestCase

from accounts.models import User


class UserManagerTests(TestCase):
    """Tests for the custom user manager."""

    def test_create_user_with_password(self):
        """Create a normal user with a normalized email and password."""

        user = User.objects.create_user(
            email="User@Example.COM",
            password="test-password",
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(user.email, "User@example.com")
        self.assertTrue(user.check_password("test-password"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_password_sets_unusable_password(self):
        """Create a normal user with an unusable password when none is given."""

        user = User.objects.create_user(
            email="nopassword@example.com",
            first_name="No",
            last_name="Password",
        )

        self.assertFalse(user.has_usable_password())

    def test_create_user_requires_email(self):
        """Raise an error when creating a user without an email."""

        with self.assertRaisesMessage(ValueError, "Email is required"):
            User.objects.create_user(
                email="",
                password="test-password",
                first_name="Test",
                last_name="User",
            )

    def test_create_superuser_sets_required_flags(self):
        """Create a superuser with staff, superuser, and active flags set."""

        user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin-password",
            first_name="Admin",
            last_name="User",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("admin-password"))

    def test_create_superuser_requires_password(self):
        """Raise an error when creating a superuser without a password."""

        with self.assertRaisesMessage(ValueError, "Superuser must have a password"):
            User.objects.create_superuser(
                email="admin@example.com",
                password="",
                first_name="Admin",
                last_name="User",
            )

    def test_create_superuser_requires_is_staff_true(self):
        """Raise an error when a superuser is created without staff access."""

        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True"):
            User.objects.create_superuser(
                email="admin@example.com",
                password="admin-password",
                first_name="Admin",
                last_name="User",
                is_staff=False,
            )

    def test_create_superuser_requires_is_superuser_true(self):
        """Raise an error when a superuser is created without superuser access."""

        with self.assertRaisesMessage(
            ValueError,
            "Superuser must have is_superuser=True",
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="admin-password",
                first_name="Admin",
                last_name="User",
                is_superuser=False,
            )

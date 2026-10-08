"""Tests for the User model."""

from django.test import TestCase

from accounts.models import User


class UserModelTests(TestCase):
    """Tests for the User model methods."""

    def test_str_returns_email(self):
        """Test that the string representation of a user returns their email."""
        user = User(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
        )

        self.assertEqual(str(user), "john.doe@example.com")

    def test_get_full_name_without_middle_name(self):
        """Test get_full_name when user has no middle name."""
        user = User(
            email="john.doe@example.com",
            first_name="John",
            middle_name="",
            last_name="Doe",
        )

        self.assertEqual(user.get_full_name(), "John Doe")

    def test_get_full_name_with_middle_name(self):
        """Test get_full_name when user has a middle name."""
        user = User(
            email="john.doe@example.com",
            first_name="John",
            middle_name="Robert",
            last_name="Doe",
        )

        self.assertEqual(user.get_full_name(), "John Robert Doe")

    def test_get_full_name_with_none_middle_name(self):
        """Test get_full_name when middle_name is None."""
        user = User(
            email="jane.smith@example.com",
            first_name="Jane",
            middle_name=None,
            last_name="Smith",
        )

        self.assertEqual(user.get_full_name(), "Jane Smith")

    def test_get_full_name_with_only_first_name(self):
        """Test get_full_name when user has only a first name."""
        user = User(
            email="single@example.com",
            first_name="Cher",
            middle_name="",
            last_name="",
        )

        self.assertEqual(user.get_full_name(), "Cher")

    def test_get_full_name_with_only_last_name(self):
        """Test get_full_name when user has only a last name."""
        user = User(
            email="anon@example.com",
            first_name="",
            middle_name="",
            last_name="Bond",
        )

        self.assertEqual(user.get_full_name(), "Bond")

    def test_get_full_name_with_persisted_user(self):
        """Test get_full_name with a user saved in the database."""
        user = User.objects.create_user(
            email="saved.user@example.com",
            password="test-password123",
            first_name="Alice",
            last_name="Wonderland",
        )

        self.assertEqual(user.get_full_name(), "Alice Wonderland")
        self.assertEqual(str(user), "saved.user@example.com")

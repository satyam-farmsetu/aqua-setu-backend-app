"""Serializer for the authenticated user's profile."""

from rest_framework import serializers

from accounts.models import User


class MeSerializer(serializers.ModelSerializer):
    """Serializer for the authenticated user's profile."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        """Meta class for MeSerializer."""

        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
        )
        read_only_fields = fields

    def get_full_name(self, obj: User) -> str:
        """Return the user's full name."""

        return obj.get_full_name()

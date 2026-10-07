from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Serializer for the login request."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

"""Serializer describing the JWT token pair response."""

from rest_framework import serializers


class TokenResponseSerializer(serializers.Serializer):
    """Response schema for JWT token pair endpoints."""

    access = serializers.CharField(help_text="JWT access token")
    refresh = serializers.CharField(help_text="JWT refresh token")

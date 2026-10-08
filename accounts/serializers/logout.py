"""Serializer that validates and blacklists a refresh token on logout."""

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError

from accounts.utils.token import get_refresh_token


class LogoutSerializer(serializers.Serializer):
    """Serializer for logging users out by blacklisting a refresh token."""

    refresh = serializers.CharField()

    def validate_refresh(self, value: str) -> str:
        """Validate that the submitted refresh token can be parsed."""

        try:
            get_refresh_token(value)
        except TokenError as exc:
            raise serializers.ValidationError("Invalid refresh token.") from exc

        return value

    def save(self, **_kwargs: object) -> None:
        """Blacklist the validated refresh token."""

        token = get_refresh_token(self.validated_data["refresh"])
        token.blacklist()

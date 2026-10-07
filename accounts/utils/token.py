from typing import Any, cast

from rest_framework_simplejwt.tokens import RefreshToken


def get_refresh_token(token: str) -> RefreshToken:
    """Build a refresh token from its encoded string."""

    return RefreshToken(cast(Any, token))

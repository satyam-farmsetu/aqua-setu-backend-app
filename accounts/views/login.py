from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import LoginSerializer, TokenResponseSerializer


@extend_schema(
    request=LoginSerializer,
    responses={
        status.HTTP_200_OK: TokenResponseSerializer,
    },
)
class LoginView(TokenObtainPairView):
    """API endpoint for obtaining JWT access and refresh tokens."""

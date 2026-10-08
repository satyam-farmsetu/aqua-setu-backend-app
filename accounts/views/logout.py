"""Logout endpoint that blacklists the given refresh token."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LogoutSerializer


class LogoutView(APIView):
    """API endpoint for blacklisting a refresh token."""

    serializer_class = LogoutSerializer

    @extend_schema(
        request=LogoutSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def post(self, request: Request, *_args: object, **_kwargs: object) -> Response:
        """Blacklist the provided refresh token."""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

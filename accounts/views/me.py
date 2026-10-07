from typing import cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from accounts.serializers import MeSerializer


class MeViewSet(GenericViewSet):
    """API endpoint for retrieving the authenticated user's profile."""

    serializer_class = MeSerializer
    http_method_names = ("get", "head", "options")

    @extend_schema(
        responses={
            status.HTTP_200_OK: MeSerializer,
        },
    )
    def retrieve(
        self,
        _request: Request,
        *_args,
        **_kwargs,
    ) -> Response:
        """Return the authenticated user's profile."""

        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self) -> User:
        """Return the authenticated user."""

        return cast(User, self.request.user)

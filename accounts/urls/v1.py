from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LoginView, LogoutView, MeViewSet

app_name = "accounts"


router = routers.DefaultRouter()

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "me/",
        MeViewSet.as_view({"get": "retrieve"}),
        name="me",
    ),
    *router.urls,
]

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from user.authentication.views import VerifyAuthAPIView, LogoutAPIView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", VerifyAuthAPIView.as_view(), name="verify-google"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]

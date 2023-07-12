from datetime import timedelta

from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.authentication.serializers import LoginSerializer, LogoutSerializer
from user.models import User


class VerifyAuthAPIView(CreateAPIView):
    model = User
    permission_classes = ()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["credential"]
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            CLIENT_ID = "895399845840-c0eisal6806qg2hgsejkh3hksno2onjb.apps.googleusercontent.com"
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            data = idinfo
            print(data)
            userid = idinfo["sub"]
        except ValueError:
            raise ValidationError(detail="Invalid Login Information")

        user = self.model.objects.filter(
            email=data["email"],
        ).first()
        if not user:
            user = User.objects.create(
                email=data["email"],
                first_name=data["given_name"],
                last_name=data["family_name"],
                image=data["picture"],
                is_customer=True,
            )
            user.save()
        return Response(self.generate_token(user))

    def generate_token(self, user):
        iat = timezone.now()
        exp = iat + timedelta(hours=1)
        exp_rf = iat + timedelta(days=90)
        token = RefreshToken.for_user(user)
        return dict(
            token=str(token.access_token),
            refresh=str(token),
            exp=int(exp.timestamp()),
            iat=int(iat.timestamp()),
            exp_rf=int(exp_rf.timestamp()),
        )


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_object = dict(message="Logout thành công")
        return Response(data=response_object, status=status.HTTP_200_OK)

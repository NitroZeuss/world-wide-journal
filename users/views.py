from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken
from knox import views as knox_views
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .serializers import RegisterSerializer, CustomAuthTokenSerializer
from .models import User
from rest_framework import generics, status
from .serializers import RegisterSerializer, VerifyOtpSerializer


# --- Login ---
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


# --- Logout ---
class LogoutAPI(knox_views.LogoutView):
    permission_classes = (permissions.IsAuthenticated,)


class LogoutAllAPI(knox_views.LogoutAllView):
    permission_classes = (permissions.IsAuthenticated,)





class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered. OTP sent to email."}, status=status.HTTP_201_CREATED)


class VerifyOtpAPI(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)






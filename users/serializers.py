from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import User, OtpToken
import random


from .models import User


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    _('Unable to log in with provided credentials.'),
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                _('Must include "username" and "password".'),
                code='authorization'
            )

        attrs['user'] = user
        return attrs




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        user.is_verified = False
        user.save()

        # create OTP for the new user
        otp = str(random.randint(100000, 999999))
        expiry = timezone.now() + timedelta(minutes=5)

        OtpToken.objects.create(
            user=user,
            otp_code=otp,
            otp_expires_at=expiry
        )

        # email send
        from django.core.mail import send_mail
        from django.conf import settings

        send_mail(
            subject="Your OTP Code",
            message=f"Welcome {user.username}! Your OTP is {otp}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data["email"]
        otp = data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user with this email.")

        try:
            otp_record = OtpToken.objects.filter(user=user).latest("id")
        except OtpToken.DoesNotExist:
            raise serializers.ValidationError("No OTP found. Please request again.")

        if otp_record.otp_code != otp:
            raise serializers.ValidationError("Invalid OTP.")
        if otp_record.otp_expires_at < timezone.now():
            raise serializers.ValidationError("OTP expired. Request a new one.")

        user.is_verified = True
        user.save()

        return data

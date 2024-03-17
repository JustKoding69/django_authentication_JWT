from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "company",
            "password",
            "password2",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise serializers.ValidationError("Password didn't match!")
        return attrs

    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name"]


class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError("Password didn't match!")
        user.set_password(password)
        user.save()
        return attrs


class UserPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:8000/api/users/" + user_id + "/" + token
            print("Encoding Link: ", link)
            print("User ID: ", user_id)
            print("Token:", token)
            body = f"Click following link to reset your password ${link}"
            data = {
                "subject": "Reset your password",
                "body": body,
                "to_email": user.email,
            }
            Util.send_mail(data)
            return attrs
        else:
            raise serializers.ValidationError("You are not registered")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user_id = self.context.get("user_id")
        token = self.context.get("token")
        if password != password2:
            raise serializers.ValidationError("Password didn't match!")
        id = smart_str(urlsafe_base64_decode(user_id))
        user = CustomUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Token is not valid")
        user.set_password(password)
        user.save()
        return attrs

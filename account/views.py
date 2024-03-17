from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserPasswordChangeSerializer,
    UserPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
)
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration successfull. Account created"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Logged in successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"errors": {"non_field_erros": ["Email or password is not valid"]}},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"msg": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserPasswordChangeSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Changed successfully"})
        return Response(
            {"msg": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password reset email sent. Check your email."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, user_id, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"user_id": user_id, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password reset successfully!"}, status=status.HTTP_200_OK
            )
        return Response(
            {"msg": "Something went wrong.Try again"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# class PasswordResetView(APIView):
#     renderer_classes = [UserRenderer]

#     def post(self, request, user_id, token, format=None):
#         serializer = PasswordResetSerializer(
#             data=request.data, context={"user_id": user_id, "token": token}
#         )
#         if serializer.is_valid(raise_exception=True):
#             return Response(
#                 {"msg": "Password reset successflly"}, status=status.HTTP_200_OK
#             )
#         return Response(
#             {"msg": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
#         )

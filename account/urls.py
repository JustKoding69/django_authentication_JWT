from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    "user-register", views.UserRegistrationView, basename="UserRegistration"
)
router.register("user-login", views.UserLoginView, basename="UserLogin")
router.register("user-profile", views.UserProfileView, basename="UserProfile")
router.register("change-password", views.PasswordChangeView, basename="UserProfile")
router.register(
    "send-password-reset-email", views.PasswordResetEmailView, basename="UserProfile"
)
router.register(
    "reset/<user_id>/<token>", views.UserPasswordResetView, basename="UserProfile"
)
urlpatterns = [
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user-register",
    ),
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="user-login",
    ),
    path(
        "user-profile/",
        views.UserProfileView.as_view(),
        name="user-profile",
    ),
    path(
        "change-password/",
        views.PasswordChangeView.as_view(),
        name="change-password",
    ),
    path(
        "send-password-reset-email/",
        views.PasswordResetEmailView.as_view(),
        name="password-reset-email",
    ),
    path(
        "reset-password/<user_id>/<token>/",
        views.UserPasswordResetView.as_view(),
        name="password-reset-email",
    ),
]

from rest_framework import permissions
from users.models import User


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешает редактировать объект только администратору или superuser
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.ADMIN or request.user.is_superuser
        )


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """
    Позволяет просматривать объект всем, аутентифицированным добавлять отзыв,
    автору, модератору, админу редактировать и удалять отзыв.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return (
            obj.author == request.user
            or request.user.role == User.ADMIN
            or request.user.role == User.MODERATOR
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == User.ADMIN
        )

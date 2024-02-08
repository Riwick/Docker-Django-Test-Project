from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author.user == request.user


class IsAdminOrStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser or request.user.is_staff


class IsUserOrSuperUserOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.id == request.user.id or (request.user.is_superuser or request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class IsSellerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.id == request.user.id

from rest_framework.permissions import BasePermission
from users.userABC import UserABC


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == UserABC.Roles.ADMIN

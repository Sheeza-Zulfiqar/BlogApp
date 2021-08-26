from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user




class IsSuperUser(IsAdminUser):
    message = 'User is not superuser'
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_superuser)
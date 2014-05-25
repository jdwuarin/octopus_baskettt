from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsOwnerOrPublic(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # permissions are only allowed to the owner of the snippet.

        if request.method in permissions.SAFE_METHODS:
            condition = obj.user == request.user or obj.is_public
            return condition

        return obj.user == request.user
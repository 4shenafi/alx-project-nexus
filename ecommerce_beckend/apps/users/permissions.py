"""
Custom permissions for NexusCommerce
"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsApprovedVendor(permissions.BasePermission):
    """
    Custom permission to only allow approved vendors.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_approved_vendor
        )


class IsVendorOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow vendors and admins.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_vendor or request.user.is_admin)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners or admins.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_admin:
            return True

        # Owners have access to their own objects
        if hasattr(obj, "user"):
            return obj.user == request.user
        elif hasattr(obj, "customer"):
            return obj.customer == request.user
        elif hasattr(obj, "vendor"):
            return obj.vendor == request.user

        return False


class IsVendorOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow vendor owners or admins.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_admin:
            return True

        # Vendor owners have access to their own objects
        if hasattr(obj, "vendor"):
            return obj.vendor == request.user

        return False


class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow read-only access to unauthenticated users,
    and full access to authenticated users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to authenticated users
        return request.user and request.user.is_authenticated

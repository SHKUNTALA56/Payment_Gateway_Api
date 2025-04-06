# permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admins to access a view.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has the 'admin' role
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'

class IsBusinessOwner(permissions.BasePermission):
    """
    Custom permission to only allow business owners to access a view.
    """
    def has_permission(self, request, view):
        return request.user.role == 'business_owner'

class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customers to access a view.
    """
    def has_permission(self, request, view):
        return request.user.role == 'customer'

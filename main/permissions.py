from rest_framework.permissions import IsAdminUser
from rest_framework import permissions

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsCompanyAdmin(permissions.BasePermission):
    message = 'None of permissions requirements fulfilled.'

    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAdminOrSuperUser(permissions.BasePermission):
    message = 'None of permissions requirements fulfilled.'

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_company_admin


class IsAuthenticatedOrSuperUser(permissions.BasePermission):
    message = 'None of permissions requirements fulfilled.'

    def has_permission(self, request, view):
        return bool(request.user or request.user.is_superuser)

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user

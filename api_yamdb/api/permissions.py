from rest_framework.permissions import (
    BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS)


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.is_authenticated
                and request.user.is_admin)


class IsModeratorOrIsOwner(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):

        return any((request.user.is_authenticated
                    and request.user.is_admin,
                    request.user.is_authenticated
                    and request.user.is_moderator,
                    obj.author == request.user,
                    request.method in SAFE_METHODS))


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        return (request.user.is_authenticated
                and request.user.is_admin
                or request.method in SAFE_METHODS)

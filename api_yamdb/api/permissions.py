from rest_framework.permissions import (
    BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS)


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)


class IsModeratorOrIsOwner(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):

        return ((request.user.is_authenticated
                 and request.user.is_admin)
                or (request.user.is_authenticated
                    and request.user.is_moderator)
                or (request.user.is_superuser)
                or (obj.author == request.user)
                or (request.method in SAFE_METHODS))

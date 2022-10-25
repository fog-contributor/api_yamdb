from rest_framework.permissions import (
    BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS)

from reviews.models import ROLE


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.is_authenticated
                and request.user.role == ROLE[2][0]
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):

        return (request.user.is_authenticated
                and request.user.role == ROLE[2][0]
                or request.user.is_superuser)


class IsModeratorOrIsOwner(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):

        return ((request.user.is_authenticated
                 and request.user.role == ROLE[2][0])
                or (request.user.is_authenticated
                    and request.user.role == ROLE[1][0])
                or (request.user.is_superuser)
                or (obj.author == request.user)
                or (request.method in SAFE_METHODS))

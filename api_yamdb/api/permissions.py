from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        return (request.user.is_authenticated)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):

        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):

        return (request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser)


class IsModeratorOrIsOwner(BasePermission):

    def has_permission(self, request, view):

        return (request.user.is_authenticated
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):

        return ((request.user.is_authenticated
                 and request.user.role == 'admin')
                or (request.user.is_authenticated
                    and request.user.role == 'moderator')
                or (request.user.is_authenticated
                    and request.user.is_superuser)
                or (request.user.is_authenticated
                    and obj.author == request.user)
                or (request.method in SAFE_METHODS))

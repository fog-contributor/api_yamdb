from rest_framework.permissions import BasePermission


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.role == 'admin'
                or request.user.is_superuser)


class IsModerator(BasePermission):
    pass

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.role.name == 'admin'
                or request.user.is_superuser)

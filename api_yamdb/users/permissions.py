from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        else:
            return request.user.is_admin

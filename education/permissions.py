from rest_framework.permissions import BasePermission


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moderator')


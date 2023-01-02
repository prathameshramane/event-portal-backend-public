from rest_framework.permissions import BasePermission


class DeskClearance(BasePermission):

    message = "Not a desk account"

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.desk:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.desk:
            return True
        return False


class EventHeadClearance(BasePermission):

    message = "Not an event head account"

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.event_head:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.event_head:
            return True
        return False


class AdminClearance(BasePermission):

    message = "Not an Admin account"

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.admin:
            return True
        return False

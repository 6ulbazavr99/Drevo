from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAccountOwner(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAccountOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj

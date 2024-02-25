from rest_framework.permissions import BasePermission


class IsMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj.user


class IsMember(BasePermission):
    def has_permission(self, request, view):
        if request.user.family_members.all():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return True
        return request.user == obj.user


class IsPlant(BasePermission):
    def has_permission(self, request, view):
        if request.user.family_members.all():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.planted_tree:
            return True
        return False

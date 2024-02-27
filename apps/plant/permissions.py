from rest_framework.permissions import BasePermission


class IsFamilyMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.families:
            return True
        return False


class IsTreePlanted(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.planted_tree:
            return True
        return False


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

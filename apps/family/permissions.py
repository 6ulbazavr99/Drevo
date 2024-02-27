from django.db.models import Q
from rest_framework.permissions import BasePermission


class IsFamilyMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user in obj.members.all()


class IsParentsMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        parents_filter = (Q(familymember__role='father') | Q(familymember__role='mother')
                          | Q(familymember__role='grandfather') | Q(familymember__role='grandmother'))
        parents = obj.members.filter(parents_filter)
        return request.user in parents

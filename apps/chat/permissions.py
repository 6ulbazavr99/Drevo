from rest_framework import permissions

class IsChatParticipant(permissions.BasePermission):
    """
    Разрешение на проверку, является ли пользователь участником чата.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли текущий пользователь участником чата
        return request.user.is_authenticated and obj.participants.filter(id=request.user.id).exists()

from rest_framework import serializers

from .models import Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        from apps.chat.models import Message  # Moved inside Meta
        model = Message
        fields = (
            'id',
            'chat',
            'sender',
            'content',
            'timestamp',
        )


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id',)

    class Meta:
        from apps.chat.models import Chat  # Moved inside Meta
        model = Chat
        fields = (
            'id',
            'participants',
            'created_at',
        )
        read_only_fields = ('id',)
        depth = 1


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id',)

    class Meta:
        model = Chat
        fields = (
            'id',
            'participants',
            'messages',
            'created_at',
        )
        read_only_fields = ('id',)
        depth = 1

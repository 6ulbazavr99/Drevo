from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.blog.models import Post, PostImage, Comment


User = get_user_model()


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    images = PostImageSerializer(many=True, required=False)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('user', 'title', 'body', 'preview', "images", 'created_at', 'likes_count', 'comments_count')

    def get_likes_count(self, instance):
        return instance.likes.count()

    def get_comments_count(self, instance):
        return instance.comments.count()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('user', 'title', 'body', 'preview', "images")

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        for image in images:
            PostImage.objects.create(image=image, post=post)
        return post


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('user', 'title', 'preview', 'created_at', 'likes_count', 'comments_count')

    def get_likes_count(self, instance):
        return instance.likes.count()

    def get_comments_count(self, instance):
        return instance.comments.count()


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Comment
        fields = ('id', 'user', 'body')


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Comment
        fields = ('user', 'body', 'created_at')


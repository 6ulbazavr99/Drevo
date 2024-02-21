from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import Post, Like, Comment
from . import permissions
from . import serializers
from rest_framework import status


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateUpdateSerializer
        elif self.action in ('retrieve'):
            return serializers.PostDetailSerializer
        elif self.action == 'comments':
            return serializers.CommentCreateUpdateSerializer
        return serializers.PostlistSerializer

    def get_permissions(self):
        if self.action in ('create', 'like'):
            return [IsAuthenticated()]
        elif self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), permissions.IsAdmin(), permissions.IsAuthor()]
        return [AllowAny()]

    @action(['GET'], detail=True)
    def like(self, request, pk=None, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if Like.objects.filter(post=post, user=user).exists():
            like = Like.objects.filter(post=post, user=user)
            like.delete()
            return Response({"message": "Like removed successfully."}, status=status.HTTP_200_OK)
        Like.objects.create(post=post, user=user)
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['GET'], detail=True)
    def get_liked_users(self, request, pk=None):
        post = self.get_object()
        liked_users = Like.objects.filter(post=post)

        serializer = serializers.UserLikeSerializer(liked_users, many=True)
        return Response({"liked_users": serializer.data})

    @action(['POST', 'PATCH', 'DELETE', 'GET'], detail=True)
    def comments(self, request, pk=None, *args, **kwargs):
        post = self.get_object()
        user = request.user
        body = request.data.get('body')
        comment_id = request.data.get('id')

        if request.method == 'POST':
            if request.user.is_authenticated:
                Comment.objects.create(post=post, user=user, body=body)
                return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        elif request.method in ['PATCH', 'DELETE']:
            if not comment_id:
                return Response({"message": "Comment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                comment = Comment.objects.get(pk=comment_id, post=post)
                if user == comment.user or user.is_staff:
                    if request.method == 'PATCH':
                        comment.body = body
                        comment.save()
                        return Response({"message": "Comment updated successfully"}, status=status.HTTP_200_OK)
                    elif request.method == 'DELETE':
                        comment.delete()
                        return Response({"message": "Comment deleted"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            except Comment.DoesNotExist:
                return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'GET':
            comments = Comment.objects.filter(post=post)
            serializer = serializers.CommentListSerializer(comments, many=True)
            return Response({"comments": serializer.data})

            


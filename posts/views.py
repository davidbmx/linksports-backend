from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .serializers import PostSerializer, ImageSerializer, VideoSerializer, PostCommentSerializer
from .models import Post, PostLike, PostComment
from users.models import User
from lib.socket_layer import SocketAction

# /api/posts/
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like_unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like_exists = PostLike.objects.filter(post=post, user_like=user)
        if like_exists.exists():
            like_exists.delete()
            post.num_likes = F('num_likes') - 1
        else:
            PostLike.objects.create(post=post, user_like=user)
            post.num_likes = F('num_likes') + 1

        post.save()
        post = self.get_object()
        serializer = PostSerializer(post, context=self.get_serializer_context(), many=False)
        actions = SocketAction('user_actions')
        actions.emit({
            'type': 'like_unlike_post',
            'post_id': serializer.data.get('id'),
            'num_likes': serializer.data.get('num_likes'),
        })
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user__uid=self.kwargs['uid'])
        return queryset
        

# /api/my_posts/
class MyPostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        user = User.objects.get(pk=self.request.user.pk)
        user.num_posts = F('num_posts') + 1
        user.save()

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_image(self, request, pk=None):
        post = self.get_object()
        serializer = ImageSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_video(self, request, pk=None):
        post = self.get_object()
        serializer = VideoSerializer(data=request.data, instance=post, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], parser_classes=[MultiPartParser])
    def comments(self, request, pk=None):
        post = self.get_object()
        serializer = PostCommentSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCommentView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = PostComment.objects.all().select_related('user')
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_post(self, post_id):
        post = get_object_or_404(Post, id=post_id)
        return post

    def list(self, request, post_id=None):
        post = self.get_post(post_id)
        queryset = self.get_queryset()
        queryset = queryset.filter(post=post)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, context=self.get_serializer_context(), many=True)
        return self.get_paginated_response(serializer.data)
    
    def create(self, request, post_id=None):
        post = self.get_post(post_id)
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)
        post.add_comment()
        post = self.get_post(post_id)
        actions = SocketAction('user_actions')
        actions.emit({
            'type': 'comment_post',
            'post_id': str(post.id),
            'num_comments': post.num_comments_formatted,
        })
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


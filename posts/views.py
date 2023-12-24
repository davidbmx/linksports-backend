from django.db.models import F
from rest_framework import viewsets, mixins, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from .serializers import PostSerializer, ImageSerializer, VideoSerializer
from .models import Post, PostLike
from users.models import User

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
        return Response({}, status=status.HTTP_201_CREATED)


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
    

from rest_framework import serializers

from .models import Post, PostImage, PostComment
from users.models import User, Following

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'uid',
            'name',
            'avatar',
            'username',
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
        read_only_fields = ['post']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['video', 'video_thumb',]

class PostSerializer(serializers.ModelSerializer):
    post_images = ImageSerializer(read_only=True, many=True)
    user = UserPostSerializer(read_only=True, many=False)
    liked = serializers.SerializerMethodField('get_liked')
    following = serializers.SerializerMethodField('get_following')
    my_post = serializers.SerializerMethodField('get_my_post')
    num_likes = serializers.SerializerMethodField('get_num_likes')
    num_views = serializers.SerializerMethodField('get_num_views')
    num_comments = serializers.SerializerMethodField('get_num_comments')

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id','user','num_likes','num_views','num_comments',]
    
    def get_user_request(self):
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        return user
    
    def get_liked(self, obj):
        user = self.get_user_request()
        if not user:
            return False
        liked = obj.post_likes.filter(user_like=user.id).exists()
        return liked
    
    def get_following(self, obj):
        user = self.get_user_request()
        if not user:
            return False
        following = Following.objects.filter(user=obj.user, user_following=user).exists()
        return following
    
    def get_my_post(self, obj):
        user = self.get_user_request()
        if not user:
            return False
        return obj.user.id == user.id
    
    def get_num_likes(self, obj):
        return obj.num_likes_formatted
    
    def get_num_views(self, obj):
        return obj.num_views_formatted
    
    def get_num_comments(self, obj):
        return obj.num_comments_formatted
    
class PostCommentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True, many=False)
    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ['post', 'user']

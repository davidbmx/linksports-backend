from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from firebase_admin import auth

from users.models import User
from lib.tools import ab_num

class UserSerializer(serializers.ModelSerializer):
    fans = serializers.SerializerMethodField('get_fans')
    posts = serializers.SerializerMethodField('get_posts')
    following = serializers.SerializerMethodField('get_following')

    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'uid',
            'fans',
            'following',
            'posts',
            'bookmarks',
            'description',
            'active',
            'password',
            'username',
            'avatar'
        ]
        read_only_fields = [
            'uid',
            'num_fans',
            'num_following',
            'num_posts',
            'bookmarks',
            'active',
            'avatar'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    
    def get_fans(self, obj):
        return ab_num(obj.num_fans)

    def get_following(self, obj):
        return ab_num(obj.num_following)
    
    def get_posts(self, obj):
        return ab_num(obj.num_posts)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])

        try:
            print(validated_data['password'])
            userFirebase = auth.create_user(
                email=user.email,
                email_verified=True,
                password=validated_data['password'],
                display_name=user.username,
            )
        except:
            user.delete()
            raise ValidationError(detail="Ocurrio un problema al momento de registrar el usuario")
        
        user.uid = userFirebase.uid
        user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('email', None)
        return super().update(instance, validated_data)

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar',]

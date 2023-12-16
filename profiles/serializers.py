from rest_framework import serializers
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'uid',
            'likes',
            'bookmarks',
            'active',
        ]
        read_only_fields = ['active', 'bookmarks', 'likes', 'user']

import os
from django.http.response import Http404
from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from users.serializers import UserSerializer, AvatarSerializer
from users.models import User, Following
from lib.tools import ab_num

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            user = User.objects.get(pk=request.user.pk)
            print(user)
        except User.DoesNotExist:
            raise Http404('Page not found')
        
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], parser_classes=[MultiPartParser])
    def avatar(self, request, uid=None):
        user = self.get_object()
        serializer = AvatarSerializer(data=request.data, instance=user, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'])
    def follow_unfollow(self, request, uid=None):
        user = self.get_object()
        rowFollow = user.user_follow.filter(user_following=request.user).first()
        if rowFollow:
            rowFollow.delete()
            user.num_fans = F('num_fans') - 1
            request.user.num_following = F('num_following') - 1
        else:
            Following.objects.create(user=user, user_following=request.user)
            user.num_fans = F('num_fans') + 1
            request.user.num_following = F('num_following') + 1

        user.save()
        request.user.save()
        user = self.get_object()
        response = {
            'is_following': not bool(rowFollow),
            'fans': ab_num(user.num_fans),
        }
        return Response(response, status=status.HTTP_201_CREATED)
        


from django.http.response import Http404
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from firebase_admin import auth

# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], authentication_classes=[])
    def register(self, request):
        print(request.data)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        username = request.data.get('username', None)
        uid = request.data.get('uid', None)

        if not (email or password or username or uid):
            raise Http404('Page not found')
        
        lookup = (
            Q(username=username) |
            Q(email=email)
        )

        userValidation = User.objects.filter(lookup).first()
        
        if userValidation:
            if userValidation.email == email:
                raise ValidationError({"detail": "Correo ya se encuentra registrado"})
            raise ValidationError({"detail": "Usuario ya se encuentra registrado"})
        
        user = User.objects.create_user(username, email, password)
        try:
            userFirebase = auth.create_user(
                email=user.email,
                email_verified=True,
                password=password,
                display_name=username,
            )
        except:
            user.delete()
            raise ValidationError(detail="Ocurrio un problema al momento de registrar el usuario")
        
        Profile.objects.create(uid=userFirebase.uid, user=user)
        return Response({'created': True}, status=status.HTTP_201_CREATED)
        
    
    
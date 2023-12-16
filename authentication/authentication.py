
from rest_framework import authentication
from rest_framework import exceptions

from profiles.models import Profile
from lib.firebase import auth


import logging
logger = logging.getLogger(__name__)

class FirebaseAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        print(1)
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
        
        auth_header_list = auth_header.split(" ")

        if(auth_header_list[0] == "Bearer"):
          return self.authenticate_on_firebase(auth_header_list[1], request)

    def authenticate_on_firebase(self, id_token, request):
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed('Invalid token')

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get('uid')
            profile = Profile.objects.get(uid=uid)
            if not profile.active:
              raise exceptions.AuthenticationFailed('User does not have permission to access')

        except Profile.DoesNotExist:
            if request.path == '/api/profiles/register/' and request.method == 'POST':
                return (None, None)
            raise exceptions.AuthenticationFailed('User does not exists')
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid user token')

        return (profile.user, None)


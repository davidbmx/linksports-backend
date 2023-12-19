from rest_framework import authentication
from rest_framework import exceptions

from users.models  import User
from lib.firebase import auth


import logging
logger = logging.getLogger(__name__)

class FirebaseAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
        
        auth_header_list = auth_header.split(" ")

        if(auth_header_list[0] == "Bearer"):
          return self.authenticate_on_firebase(auth_header_list[1], request)
        return None

    def authenticate_on_firebase(self, id_token, request):
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get('uid')
            print(uid)
            user = User.objects.get(uid=uid)
            if not user.active:
              raise exceptions.AuthenticationFailed('User does not have permission to access')

        except User.DoesNotExist:
            if request.path == '/api/users/' and request.method == 'POST':
                return None
            raise exceptions.AuthenticationFailed('User does not exists')
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid user token')

        return (user, None)


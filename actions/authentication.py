from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from users.models  import User
from lib.firebase import auth

@database_sync_to_async
def get_user(querystring):
    querystring = querystring.split('=')
    if len(querystring) <= 0:
        return AnonymousUser()
    
    id_token = querystring[1]
    decoded_token = None
    
    try:
        decoded_token = auth.verify_id_token(id_token)
    except Exception as e:
        return AnonymousUser()

   
    if not id_token or not decoded_token:
        return AnonymousUser()

    try:
        uid = decoded_token.get('uid')
        user = User.objects.get(uid=uid)
        if not user.active:
            return AnonymousUser()

    except User.DoesNotExist:
        return AnonymousUser()
    except Exception as e:
        return AnonymousUser()

    return user

class FirebaseMiddleware:
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, scope, receive, send):
        # Obtener el token del scope
        querystring = scope.get("query_string").decode("utf-8")

        scope['user'] = await get_user(querystring)
        return await self.app(scope, receive, send)
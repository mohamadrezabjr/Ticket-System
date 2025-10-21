import jwt
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from auth_app.models import User


@database_sync_to_async
def get_user(token):
    try :
        UntypedToken(token)
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token["user_id"]
        user = User.objects.get(id=user_id)
        return user
    except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
        return None

class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        auth_header = headers.get(b'authorization', None)

        user = None
        if auth_header :
            token_str = auth_header.decode()
            token = token_str.split()[1]
            user = await get_user(token)

        scope['user'] = user or AnonymousUser()

        return await super().__call__(scope, receive, send)
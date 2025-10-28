from urllib.parse import parse_qs

import jwt
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async



@database_sync_to_async
def get_user(token):
    from auth_app.models import User
    from django.conf import settings
    from rest_framework_simplejwt.tokens import UntypedToken
    from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, ExpiredTokenError
    from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
    try :
        UntypedToken(token)
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token["user_id"]
        user = User.objects.get(id=user_id)
        return user
    except (InvalidToken,TokenError, InvalidTokenError,ExpiredSignatureError, User.DoesNotExist, ExpiredTokenError):
        return None

class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")[0]

        user = None
        if token :
            user = await get_user(token)
        scope['user'] = user or AnonymousUser()

        return await super().__call__(scope, receive, send)
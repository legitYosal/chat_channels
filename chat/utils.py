
from channels.db import database_sync_to_async
from .exceptions import ClientError
from accounts.models import User

@database_sync_to_async
def get_user_matches(user_name, user):
    if not user.is_authenticated:
        raise ClientError('USER_HAS_TO_LOGIN')

    try:
        matches = User.objects.filter(username__contains=user_name)[:10]
    except User.DoesNotExist:
        raise ClientError('NO_MATCH')
    print('log matches are ', matches)
    return [[user.username, user.is_online] for user in matches]

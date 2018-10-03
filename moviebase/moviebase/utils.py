from moviebase.serializers import UserSerializer

def my_jwt_response_handler(token, user=None, request=None):
    """
    Custom JWT response to include user's serialized data.
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

from django_ecommerce.settings import SECRET_KEY

User = get_user_model()

class JwtAuthentcation(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
            # raise ValueError('token not provided')
        
        try:
            token = auth_header.split(' ')[-1]
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
            print('____________payload\n', payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token time expired')
        except jwt.InvalidKeyError:
            raise AuthenticationFailed('invalid key') # you can add more exception if you want
        
        try:
            user = User.objects.get(id = payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('user does not exists')
        
        return (user, None) 
    # as the rest_framework expect the tuple to be return not a single value and in jwt we don't need another value so that why its None
    # and i have return the user object as the DRF expect the user object not just the user id

class Dispatch:
    def get_request(self, request):
        auth = JwtAuthentcation()
        user, _ = auth.authenticate(request=request)
        if user is None:
            raise AuthenticationFailed('user not found')
        return user
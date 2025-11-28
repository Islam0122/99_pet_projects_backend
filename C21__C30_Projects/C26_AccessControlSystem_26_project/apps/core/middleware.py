import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from apps.users.models import User


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user = self.authenticate_token(token)
            if user:
                request.user = user
            else:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response

    def authenticate_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')

            if not user_id:
                return None

            user = User.objects.get(id=user_id, is_active=True)
            return user

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except User.DoesNotExist:
            return None
        except Exception:
            return None


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            user_info = f"User: {request.user}" if hasattr(request, 'user') else "Anonymous"
            print(f"[REQUEST] {request.method} {request.path} | {user_info}")

        response = self.get_response(request)

        if settings.DEBUG:
            print(f"[RESPONSE] {request.method} {request.path} | Status: {response.status_code}")

        return response

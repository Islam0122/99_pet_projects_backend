from ninja.security import HttpBearer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from ninja_extra import Router
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth
from .models import UserToken, UserProfile
from .serializers import (
    UserRegisterSchema,
    UserLoginSchema,
    UserSchema,
    TokenSchema,
    CustomTokenSchema,
    UserDetailSchema,
    UserProfileUpdateSchema,
    ErrorSchema,
    MessageSchema
)

router = Router()

jwt_auth = JWTAuth()

class CustomTokenAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_token = UserToken.objects.select_related('user').get(
                token=token,
                is_active=True
            )
            return user_token.user
        except UserToken.DoesNotExist:
            return None


custom_token_auth = CustomTokenAuth()


@router.post("/register", response={200: TokenSchema, 400: ErrorSchema}, tags=["Authentication"])
def register(request, data: UserRegisterSchema):
    if User.objects.filter(username=data.username).exists():
        return 400, {"detail": "Username already exists"}

    user = User.objects.create(
        username=data.username,
        email=data.email or '',
        password=make_password(data.password)
    )

    UserProfile.objects.create(user=user)

    refresh = RefreshToken.for_user(user)

    return 200, {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


@router.post("/login", response={200: TokenSchema, 401: ErrorSchema}, tags=["Authentication"])
def login(request, data: UserLoginSchema):
    user = authenticate(username=data.username, password=data.password)

    if not user:
        return 401, {"detail": "Invalid credentials"}

    refresh = RefreshToken.for_user(user)

    return 200, {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


@router.post("/register-custom", response={200: CustomTokenSchema, 400: ErrorSchema}, tags=["Authentication"])
def register_custom(request, data: UserRegisterSchema):
    if User.objects.filter(username=data.username).exists():
        return 400, {"detail": "Username already exists"}

    user = User.objects.create(
        username=data.username,
        email=data.email or '',
        password=make_password(data.password)
    )

    UserProfile.objects.create(user=user)

    user_token = UserToken.create_for_user(user)

    return 200, {
        "token": user_token.token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@router.post("/login-custom", response={200: CustomTokenSchema, 401: ErrorSchema}, tags=["Authentication"])
def login_custom(request, data: UserLoginSchema):
    user = authenticate(username=data.username, password=data.password)

    if not user:
        return 401, {"detail": "Invalid credentials"}

    UserToken.objects.filter(user=user, is_active=True).update(is_active=False)
    user_token = UserToken.create_for_user(user)

    return 200, {
        "token": user_token.token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@router.get("/profile", response={200: UserDetailSchema, 401: ErrorSchema}, auth=jwt_auth, tags=["Profile"])
def get_profile(request):
    user = request.auth

    profile = None
    if hasattr(user, 'profile'):
        profile = {
            "bio": user.profile.bio,
            "avatar": user.profile.avatar,
            "created_at": user.profile.created_at,
            "updated_at": user.profile.updated_at
        }

    return 200, {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile": profile
    }


@router.put("/profile", response={200: UserDetailSchema, 401: ErrorSchema}, auth=jwt_auth, tags=["Profile"])
def update_profile(request, data: UserProfileUpdateSchema):
    user = request.auth

    profile, created = UserProfile.objects.get_or_create(user=user)

    if data.bio is not None:
        profile.bio = data.bio
    if data.avatar is not None:
        profile.avatar = data.avatar

    profile.save()

    return 200, {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile": {
            "bio": profile.bio,
            "avatar": profile.avatar,
            "created_at": profile.created_at,
            "updated_at": profile.updated_at
        }
    }


@router.get("/profile-custom", response={200: UserDetailSchema, 401: ErrorSchema}, auth=custom_token_auth,
            tags=["Profile"])
def get_profile_custom(request):
    user = request.auth

    if not user:
        return 401, {"detail": "Invalid token"}

    profile = None
    if hasattr(user, 'profile'):
        profile = {
            "bio": user.profile.bio,
            "avatar": user.profile.avatar,
            "created_at": user.profile.created_at,
            "updated_at": user.profile.updated_at
        }

    return 200, {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile": profile
    }


@router.post("/logout-custom", response={200: MessageSchema, 401: ErrorSchema}, auth=custom_token_auth,
             tags=["Authentication"])
def logout_custom(request):
    user = request.auth

    if not user:
        return 401, {"detail": "Invalid token"}

    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
        UserToken.objects.filter(token=token, user=user).update(is_active=False)

    return 200, {"message": "Successfully logged out"}

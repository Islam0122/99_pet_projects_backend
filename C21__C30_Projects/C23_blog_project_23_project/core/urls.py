from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
# from apps.users.api import router as users_router
# from apps.blog.api import router as blog_router
# from django_ninja_jwt.views import TokenObtainPairView, TokenRefreshView

api = NinjaAPI()

# api.add_router("/users/", users_router)
# api.add_router("/blog/", blog_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

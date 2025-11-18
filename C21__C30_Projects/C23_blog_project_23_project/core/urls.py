from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.users.api import router as users_router
# from apps.blog.api import router as blog_router

api = NinjaAPI(
    title="Blog API",
    version="1.0.0",
    description="API для блога с Django Ninja 1.4+"
)

api.add_router("/users/", users_router, tags=["Users"])
# api.add_router("/blog/", blog_router, tags=["Blog"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

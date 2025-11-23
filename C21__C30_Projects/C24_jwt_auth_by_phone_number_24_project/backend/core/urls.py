from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.user import views
from .drf_yasg import urlpatterns as urls_swagger
from rest_framework.routers import DefaultRouter

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('app.user.urls'))
              ] + urls_swagger
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]


from django.urls import path
from .views import FairyTaleListCreateView

urlpatterns = [
    path("fairytales/", FairyTaleListCreateView.as_view(), name="fairytales"),
]

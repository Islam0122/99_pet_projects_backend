from django.http.response import HttpResponse
from rest_framework import viewsets
from .serializers import LinkSerializer
from django.shortcuts import get_object_or_404, redirect
from .models import Link
from django.utils import timezone

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


def redirect_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code)

    if link.expires_at is None or link.expires_at > timezone.now():
        link.clicks += 1
        link.save()
        return redirect(link.original_url)
    else:
        link.is_active = False
        link.save()
        return HttpResponse("Ссылка истекла или недействительна.", status=404)
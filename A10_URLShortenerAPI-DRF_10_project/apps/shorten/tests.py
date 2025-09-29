import pytest
from django.utils import timezone
from datetime import timedelta
from apps.shorten.models import Link

@pytest.mark.django_db
def test_link_creation():
    link = Link.objects.create(
        original_url="https://example.com",
        short_code="abc123"
    )
    assert link.original_url == "https://example.com"
    assert link.clicks == 0
    assert link.is_valid
    assert (link.expires_at - timezone.now()) <= timedelta(minutes=15)

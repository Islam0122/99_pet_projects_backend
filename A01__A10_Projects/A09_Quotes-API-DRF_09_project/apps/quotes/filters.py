import django_filters
from .models import Quote


class QuoteFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    tag = django_filters.CharFilter(field_name="tags__name", lookup_expr="icontains")
    text = django_filters.CharFilter(field_name="text", lookup_expr="icontains")

    class Meta:
        model = Quote
        fields = ["author", "tag", "text"]

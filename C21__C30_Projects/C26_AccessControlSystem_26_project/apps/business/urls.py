from django.urls import path
from .mock_views import (
    products_list_create,
    products_detail,
    orders_list_create,
    stores_list
)

urlpatterns = [
    path('products/', products_list_create, name='products-list-create'),
    path('products/<int:pk>/', products_detail, name='products-detail'),
    path('orders/', orders_list_create, name='orders-list-create'),
    path('stores/', stores_list, name='stores-list'),
]
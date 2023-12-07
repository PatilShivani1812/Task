from django.urls import path
from .views import (
    CustomerListCreateView, CustomerUpdateView,
    ProductListCreateView, ProductUpdateView,
    OrderListCreateView, OrderDetailView,
    OrderItemCreateView, OrderItemDetailView
)

urlpatterns = [
    path('api/customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('api/customers/<int:pk>/', CustomerUpdateView.as_view(), name='customer-update'),
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('api/orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('api/orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('api/order-items/', OrderItemCreateView.as_view(), name='order-item-create'),
    path('api/order-items/<int:pk>/', OrderItemDetailView.as_view(), name='order-item-detail'),
]

from rest_framework.routers import DefaultRouter
# myproject/urls.py
from django.urls import path

from product.views.category import CategoryDetailView, CategoryListCreateView
from product.views.product import ProductDetailView, ProductListCreateView


router = DefaultRouter()

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<uuid:pk>/cancel', CategoryDetailView.cancel, name='cancel'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<uuid:pk>/cancel', ProductDetailView.cancel, name='cancel'),


]
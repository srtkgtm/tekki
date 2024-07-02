from django.urls import path
from .views import ProductView, CreateProductView, EditProductView, DeleteProductView, MaxRetrievedProductView, DetailProductView

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/create', CreateProductView.as_view(), name='products_create'),
    path('products/<int:pk>/edit', EditProductView.as_view(), name='products_edit'),
    path('products/<int:pk>/', DetailProductView.as_view(), name='products_details'),
    path('products/<int:pk>/delete', DeleteProductView.as_view(), name='products_delete'),
    path('products/maxretrieved', MaxRetrievedProductView.as_view(), name='products_max_retrieved')
]
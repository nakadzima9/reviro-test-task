from django.urls import path
from management import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name='company-list'),
    path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='company'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product'),
]

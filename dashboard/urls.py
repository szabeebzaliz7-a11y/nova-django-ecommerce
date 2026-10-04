from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("products/", views.product_manage, name="products"),
    path("products/add/", views.product_create, name="product_add"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("categories/", views.category_manage, name="categories"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("banners/", views.banner_manage, name="banners"),
    path("banners/add/", views.banner_create, name="banner_add"),
    path("banners/<int:pk>/edit/", views.banner_edit, name="banner_edit"),
    path("banners/<int:pk>/delete/", views.banner_delete, name="banner_delete"),
]

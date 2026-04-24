from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Product Management
    path('add-product/', views.add_product, name='add-product'),  # Add a new product (for superusers and sellers)
    path('edit-product/<int:pk>/', views.edit_product, name='edit-product'),  # Edit an existing product
    path('products/', views.product_list, name='product_list'),  # View all products (for superusers)
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),  # Delete a product (for superusers)

    # Authentication
    path('login/', views.login_user, name='login'),  # User login
    path('logout/', views.logout_user, name='logout'),  # User logout
    path('register/', views.register_user, name='register'),  # User registration

    # Profile
    path('edit-profile/', views.edit_profile, name='edit-profile'),  # Edit user profile

    # Static Pages
    path('about/', views.about, name='about'),  # About page

    # Category and Product View
    path('category/<str:key>/', views.category, name='category'),  # View products by category
    path('product/<int:pk>/', views.product, name='product'),  # View individual product
]

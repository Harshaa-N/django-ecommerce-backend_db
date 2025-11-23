from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart_detail, name='cart-detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart-add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart-update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart-remove'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('wishlist/', views.wishlist_list, name='wishlist-list'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order-success'),  # For success page
]


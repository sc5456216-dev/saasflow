# Update apps/products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<path:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<path:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.cart_count, name='cart_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order/<int:order_id>/detail/', views.order_detail, name='order_detail'),
    path('track-order/', views.track_order, name='track_order'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('orders/', views.order_history, name='order_history'),
    # Review URLs
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('api/reviews/<int:product_id>/', views.get_product_reviews, name='get_product_reviews'),
    # Wishlist URLs
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/count/', views.wishlist_count, name='wishlist_count'),
    # Recently Viewed URLs
    path('recently-viewed/', views.recently_viewed, name='recently_viewed'),
    # Search URLs
    path('search/autocomplete/', views.search_autocomplete, name='search_autocomplete'),
]

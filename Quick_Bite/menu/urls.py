from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path(
        'cart/increase/<int:product_id>/',
        views.cart_increase,
        name='cart_increase',
    ),
    path(
        'cart/decrease/<int:product_id>/',
        views.cart_decrease,
        name='cart_decrease',
    ),
    path(
        'cart/remove/<int:product_id>/',
        views.cart_remove,
        name='cart_remove',
    ),
    path(
        'cart/update/<int:product_id>/',
        views.cart_update,
        name='cart_update',
    ),
]

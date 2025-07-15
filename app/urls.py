from django.contrib import admin
from django.urls import path,include
from . import views

# app_name = "payments"

urlpatterns = [
    path('', views.home,name="home"),
    path('guarantee/', views.Guarantee,name="guarantee"),
    path('payment_method/', views.Payment_method,name="payment_method"),
    path('transport/', views.Transport,name="transport"),
    path('stores/', views.store_list,name="store_list"),
    path('contract/', views.contract,name="contract"),
    path('intro/', views.intro,name="intro"),
    path('products/', views.list_product,name="list_product"),
    path('search/', views.search_items,name="search"),
    path('cart/', views.cart, name="cart"),
    path('register/', views.register, name="register"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpage, name="logout"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path("create/", views.create_order_view, name="create_order"),
    path("momo/create/<str:order_id>/", views.momo_create_payment, name="momo_create"),
    path("notify/", views.momo_notify_view, name="momo_notify"),

    path("payment/cod/", views.cod_payment_view, name="cod_payment"),
    path('payment/vnpay/<str:order_id>/', views.vnpay_create_payment, name='vnpay_create'),
    path('payment/vnpay-return/', views.vnpay_return_view, name='vnpay_return')
]
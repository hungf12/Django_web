from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
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
    path('product/<int:product_id>/', views.product_detail, name='product_detail')
]
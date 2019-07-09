from django.urls import path
from . import views

app_name = 'Shoppy'
urlpatterns =[
   path('home/', views.home, name='shoppy-home'),
   path('cart/', views.cart, name='shoppy-cart'),
   path('register/', views.buyer_register, name='shoppy-buyer-reg'),
   path('login/', views.login, name='shoppy-login'),
   path('productdetails/',views.productDetails, name='shoppy-product_details'),



]






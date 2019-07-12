from django.urls import path

from . import views


app_name = 'Shoppy'
urlpatterns =[
   path('home/', views.home, name='shoppy-home'),
   path('cart/', views.cart, name='shoppy-cart'),
   path('register/', views.buyer_register, name='shoppy-buyer-reg'),
   path('seller_register/', views.seller_register, name='shoppy-seller-reg'),
   path('login/', views.user_login, name='shoppy-login'),
   path('logout/', views.logout_view, name='shoppy-logout'),
   path('product_details', views.productDetails, name='shoppy-product_details'),
   path('seller_home/' , views.seller_home, name='shoppy-seller-home' ),
   path('user_account/' , views.user_account, name='shoppy-user_account' ),


]






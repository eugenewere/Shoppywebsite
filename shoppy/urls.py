from django.urls import path
from . import views

urlpatterns = [
   path('home/', views.home, name='shoppy-home'),
   path('productdetails/',views.productDetails, name='shoppy-product_details'),
]
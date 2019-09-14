from django.urls import path
from django.conf.urls import include, url
from androidAuthApi import views
from rest_framework.authtoken import views as authviews


urlpatterns = [
    path('login/',views.login),
    path('users/', views.UserList.as_view()),
    path('user/details/<int:pk>/', views.UserDetail.as_view()),
    path('api-token-auth/', authviews.obtain_auth_token),
    path('signup/',views.signup2),
    path('login/',views.login),
    path('category/',views.CategoryList.as_view()),
    path('unfilteredcategory/',views.UnfilteredCategoryList.as_view()),
    path('product/',views.ProductList.as_view()),
    path('wishlist/',views.WishList.as_view()),
    path('region/',views.RegionList.as_view()),
    path('product/category/',views.ProductDetails.as_view()),
    path('allProducts/',views.AllProductList.as_view()),
    path('orders/',views.OrderProductList.as_view()),
    path('androidproducts/',views.AndroidProductList.as_view()),
    path('androidproducts/<int:pk>/',views.AndroidProductDetails.as_view()),
    path('addtocart/<int:product_id>/',views.addtocart),
    path('removefromcart/<int:order_id>/',views.removefromcart),
    path('updatecart/<int:order_id>/',views.updatecart),
    path('getcartproducts/',views.getcartproducts),
    path('addtowishlist/<int:product_id>/',views.addtowishlist),
    path('getwishlistproducts/',views.getwishlistproducts),
    path('removefromwishlist/<int:wishlist_id>/',views.removefromwishlist),
    path('getproducts/',views.getproducts),
    path('checkout/<int:region_id>/',views.checkout),




]


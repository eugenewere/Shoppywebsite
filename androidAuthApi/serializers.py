from rest_framework import serializers
from shoppy.models import Buyer, Category, Product, Order_Product, Brand, Wishlist, Region, Checkout
from .models import AndroidProducts

class buyersSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Buyer
        fields = ('id', 'username')

class wishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Wishlist
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order_Product
        fields = ('id','buyer','product','checkout','quantity','total','created_at',)

class ProductSerializer(serializers.ModelSerializer):
    # orders = OrderProductSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id','name','unit_cost','product_brand','short_description','featured_url',)   


class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=False)

    class Meta:
        model = Brand
        fields = ('id','name','products')

class AndroidProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = AndroidProducts
        fields = ('id','name','unit_cost','product_brand','short_description','featured_url','category')

class AllProductsSerializer(serializers.ModelSerializer):
    androidproducts = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('name','androidproducts',)

class CategorySerializer(serializers.ModelSerializer):
    # brands = BrandSerializer(many=True, read_only=False)

    class Meta:
        model = Category
        fields = ('id','name','brands',)

class RegionSerializer(serializers.ModelSerializer):
    # brands = BrandSerializer(many=True, read_only=False)

    class Meta:
        model = Region
        fields = ('id','name',)

class CustomCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit_cost = serializers.FloatField()
    product_brand = serializers.CharField()
    short_description = serializers.CharField()
    featured_url = serializers.CharField()
    order_id = serializers.IntegerField()
    quantity = serializers.FloatField()
    total = serializers.FloatField()

class CustomWishlistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit_cost = serializers.FloatField()
    product_brand = serializers.CharField()
    short_description = serializers.CharField()
    featured_url = serializers.CharField()
    wishlist_id = serializers.IntegerField()

class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkout
        fields = '__all__'


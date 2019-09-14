from shoppy.models import Buyer, Category, Product, Order_Product, Wishlist, Checkout, Region
from .models import AndroidProducts
from .serializers import buyersSerializer, CategorySerializer, ProductSerializer, OrderProductSerializer
from .serializers import  AllProductsSerializer, AndroidProductSerializer, CustomCartSerializer, wishlistSerializer, CustomWishlistSerializer
from .serializers import RegionSerializer, CheckoutSerializer
from rest_framework import generics
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, FloatField, IntegerField
from django.utils.crypto import get_random_string


# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404


class UserList(generics.ListAPIView):
    queryset = Buyer.objects.all()
    serializer_class = buyersSerializer
    permission_classes = [IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Buyer.objects.all()
    serializer_class = buyersSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.filter(parent_id__isnull=True)
    serializer_class = CategorySerializer

class UnfilteredCategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AllProductList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = AllProductsSerializer

class AndroidProductList(generics.ListAPIView):
    queryset = AndroidProducts.objects.all()
    serializer_class = AndroidProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

class AndroidProductDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = AndroidProducts.objects.all()
    serializer_class = AndroidProductSerializer
    


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class WishList(generics.ListAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = wishlistSerializer

class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
 

class ProductDetails(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # def get_queryset(self):
    #     category = self.kwargs['category']
    #     if category is not None:
    #         return Product.objects.filter(brand= category)
    #     else:
    #         return Product.objects.all()

class OrderProductList(generics.ListAPIView):
    queryset = Order_Product.objects.all()
    serializer_class = OrderProductSerializer
 
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup2(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    email = request.data.get("email", "")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")
    phone_number = request.data.get("phone_number", "")
    if not username and not password and not email and not first_name and not last_name:
        return Response(
            data={
                "message": "username, password and email is required to register a user"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    new_buyer = Buyer.objects.create_user(
        # user_ptr_id=new_buyer.id,
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        is_staff=False
    )
    context = {
        'message': 'You Have Been Successfully Registered'
    }
    return Response(context,status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        context = {
            'error': 'Invalid Username or Password',
        }
        return Response(context, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    context = {
        'token': token.key,
        'id': user.id,
        'username': username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    return Response(context,
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addtocart(request, product_id):
    # print(request.META['HTTP_AUTHORIZATION'])
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    print(new_token)
    product = Product.objects.filter(id=product_id).first()
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    quantity = request.data.get("quantity")
    amount = product.unit_cost
    if not product_id and not quantity:
        return Response(
            data={
                "Message": "Make Sure All The Fields Are Included"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    new_OrderProduct = Order_Product.objects.create(
        product=product,
        buyer=buyer,
        quantity=quantity,
        total=(float(amount)*float(quantity)),
    )
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_201_CREATED)
        

    

@csrf_exempt
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def removefromcart(request, order_id):
    cart_product = Order_Product.objects.filter(id=order_id).first()
    cart_product.delete()
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def updatecart(request, order_id):
    print(order_id)
    current_orderproduct = Order_Product.objects.filter(id = order_id).first()
    quantity = request.data.get("quantity",)
    product = Product.objects.filter(id =current_orderproduct.product.id).first()
    amount = product.unit_cost
    if not quantity:
        return Response(
            data={
                "Message": "Make Sure All The Fields Are Included"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    current_orderproduct.quantity = quantity
    current_orderproduct.total = float(amount)*float(quantity)
    current_orderproduct.save()
 
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getcartproducts(request):
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addtowishlist(request, product_id):
    # print(request.META['HTTP_AUTHORIZATION'])
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    product = Product.objects.filter(id=product_id).first()
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not product_id:
        return Response(
            data={
                "Message": "Product does not exist"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    new_wishlistProduct = Wishlist.objects.create(
        product=product,
        buyer=buyer,
    )

    productID = Wishlist.objects.filter(buyer=buyer)
    for order in productID:
        Wishlist_product = Product.objects.filter(id = order.product.id).annotate(wishlist_id=Sum(order.id, output_field=IntegerField())).first()
        products.append(Wishlist_product)
    data = CustomWishlistSerializer(products, many=True)    
    context = {
        'data': data.data
    }
    return Response(data.data,status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getwishlistproducts(request):
    # print(request.META['HTTP_AUTHORIZATION'])
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not buyer:
        return Response(
            data={
                "Message": "You are not logged in"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    wishlistProducts = Wishlist.objects.filter(buyer=buyer)
    for order in wishlistProducts:
        allwishlistproducts = Product.objects.filter(id = order.product.id).annotate(wishlist_id=Sum(order.id, output_field=IntegerField())).first()
        products.append(allwishlistproducts)
    data = CustomWishlistSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def removefromwishlist(request, wishlist_id):
    products = []
    wishlist_product = Wishlist.objects.filter(id=wishlist_id).first()
    wishlist_product.delete()
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not buyer:
        return Response(
            data={
                "Message": "You are not logged in"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    wishlistProducts = Wishlist.objects.filter(buyer=buyer)
    for order in wishlistProducts:
        allwishlistproducts = Product.objects.filter(id = order.product.id).annotate(wishlist_id=Sum(order.id, output_field=IntegerField())).first()
        products.append(allwishlistproducts)
    data = CustomWishlistSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getproducts(request):
    category = request.data.get("name")
    print(category)
    categories = Category.objects.filter(name = category).first()
    products = AndroidProducts.objects.filter(category = categories.id)
    data = ProductSerializer(products, many = True)
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def checkout(request, region_id):
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    new_region_id = Region.objects.filter(id = region_id).first()
    if not region_id:
        return Response(
            data={
                "Message": "You have to pick a region"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    new_checkoutorder = Checkout.objects.create(
        buyer = buyer,
        region = new_region_id,
        phonenumber = buyer.phone_number,
        city = "Nairobi",
        reference_code = get_random_string(length=9),
    )
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True).update(
        checkout = new_checkoutorder.id
    )
    # checkouts = Checkout.objects.filter(id = new_checkoutorder.id).first()
    data = CheckoutSerializer([new_checkoutorder], many=True)    
    context = {
        'data': data.data
    }
    return Response(data.data,status=status.HTTP_201_CREATED)








# class GetCartProducts(generics.ListAPIView):
#     queryset = Order_Product.objects.filter(checkout__isnull=True)
#     serializer_class = OrderProductSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         r_token = request.META['HTTP_AUTHORIZATION']
#         new_token = r_token.split(' ', 1)[1]
#         token = Token.objects.filter(key=new_token).first()
#         buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
#         queryset = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
#         q =OrderProductSerializer(queryset, many=True)

#         return Response(q.data)
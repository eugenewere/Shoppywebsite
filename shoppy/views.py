from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.views.generic import View
from django.contrib.auth.models import User
from pylint.checkers.typecheck import _

from shoppy.models import *
from .forms import *
from django.http import HttpResponse, HttpResponseNotFound, request
import datetime

# Create your views here.

def search(request):
    if request.method=="POST":
        search_text = request.POST['search_text']

    else:
        search_text =""
    products = Product.objects.filter(name__contains=search_text)
    context={
        'products': products,
        'search_text': search_text,
    }
    return render_to_response('shoppy/search.html',context)

def home(request):
    user = request.user
    carousels =Carousel.objects.order_by("-created_at")
    products = Product.objects.order_by("?")[:10]
    featured_product = Product.objects.filter(status='FEATURED')
    products_all = Product.objects.all()
    wishlist_count = Wishlist.objects.filter(buyer_id=request.user.id).count()



    context ={
        'title':'Shoppy-Home',
        'user': user,
        'carousels' : carousels,
        'featured_products': featured_product,
        'products': products,
        'products_all':products_all,
        'wishlist_count':wishlist_count,
        # 'categories':categories,
        # 'orderproducts': orderproducts
    }
    return render(request, 'shoppy/home.html', context)

@login_required()
def addToWishlist(request, product_id, source):

    product = Product.objects.filter(id=product_id).first()
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    print(buyer)
    print(product)

    if buyer is not None and product is not None:
        Wishlist.objects.create(buyer=buyer, product=product)
        messages.success(request, 'Added successfully')
    else:
        messages.error(request, 'Could not add product')


    source = source.replace('____', '/')
    return redirect(source)


@login_required()
def unWishProduct(request, wishlist_id, source):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    wishlist = Wishlist.objects.filter(id=wishlist_id)
    if buyer is not None:
        wishlist.delete()
        messages.success(request, 'Your Wish Have Been Dumped')
    source = source.replace('____', '/')
    return redirect(source)


@login_required()
def unWish_All_Products(request):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    wishlist = Wishlist.objects.all().filter(buyer_id=request.user.id)
    if buyer is not None:

        wishlist.delete()
        messages.success(request, 'All Your Wishes Have Been Dumped')
    return redirect('Shoppy:shoppy-user_account')

# cart
def cart(request):
    carts = Order_Product.objects.filter(buyer_id=request.user.id)
    print(cart)
    context = {
        'carts' : carts,
        'title': 'Shoppy-Cart',
    }
    return render(request, 'shoppy/cart.html', context)

@login_required()
def addCart(request, product_id):
    print(request.POST['quantity'])
    product = Product.objects.filter(id=product_id).first()
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()

    if request.method == 'POST':
        quantity = request.POST['quantity']
        unit_cost = request.POST['unit_cost']
        total = (float(unit_cost) * float(quantity))
        request.POST = request.POST.copy()
        # request.POST['total'] = total
        request.POST['buyer'] = buyer


        orderProduct = Order_Product.objects.create(
            product=product,
            buyer=buyer,
            quantity=quantity,
            total=total,
        )
        for variantoption in request.POST.getlist('variant_options[]'):
            variant_option = Variant_Option.objects.filter(id=int(variantoption)).first()

            if variant_option is not None:
                OrderProductVariantOption.objects.create(
                    variantOptions=variant_option,
                    orderProduct=orderProduct,
                )

        messages.success(request, 'Product Added To Cart')
        return redirect('Shoppy:shoppy-home')
    return redirect('Shoppy:shoppy-home')

def deleteCartProduct(request, order_id):
    cart_product = Order_Product.objects.filter(id=order_id).first()
    cart_product.delete()
    return redirect("Shoppy:shoppy-cart")


def productDetails(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    images = Image.objects.filter(product= product_id)
    review_images = Image.objects.filter(product=product_id)[:2]
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    product_carts = Product.objects.filter(id=product_id)
    similar_products= Product.objects.filter( product_brand=product.product_brand)

    context={
        'product' : product,
        'images' : images,
        'review_images': review_images,
        'similar_products':similar_products,
        'product_carts': product_carts,
        'reviews': reviews
    }

    return render(request, 'shoppy/product_details.html',context)

def productsList(request):

    return render(request, 'shoppy/view_products/all_products.html')




def productReview(request, product_id):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    product = Product.objects.filter(id=product_id).first()
    print(product_id)
    products = Product.objects.all()
    images = Image.objects.filter(product=product_id)
    review_images = Image.objects.filter(product=product_id)[:2]
    reviews = Review.objects.filter(product=product)
    print(reviews)

    if buyer is not None:
        if request.method == 'POST':
            ratings = request.POST.get('ratings', False)
            comments = request.POST['comments']

            Review.objects.create(
                buyer=buyer,
                product=product,
                ratings=ratings,
                comments=comments,
            )
            messages.success(request, 'Your Review Was Taken')
            return redirect("Shoppy:shoppy_product_details")

    context = {
        'product': product,
        'images': images,
        'review_images': review_images,
        'reviews': reviews,
    }

    messages.error(request,'Only Buyers can Review')
    return render(request, 'shoppy/product_details.html', context)


# def user_account_product(request, product_id):
#     similar =Product.objects.filter(id=product_id).first()
#     product = Product.objects.filter(product_brand=similar.product_brand)
#     context={
#         'product':product,
#     }
#     return render(request, 'shoppy/user_account.html', context)


def user_account(request):
    user = request.user
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    seller = Seller.objects.filter(user_ptr_id=user.id).first()
    wishlist = Wishlist.objects.filter(buyer_id=request.user.id)


    if buyer is not None:
        logged_in_user = 'buyer'
    elif seller is not None:
        logged_in_user = 'seller'

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        if buyer is not None:
            user = User.objects.get(pk=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()
            Buyer.objects.filter(user_ptr_id = user.id).update(
                phone_number = phone_number,
            )
    context ={
        'user': logged_in_user,
        'wishlist': wishlist,
    }
    return render(request,'shoppy/user_account.html',context)




def buyer_register(request):
    user= request.user
    if request.method == 'POST':


        form = BuyerSignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST['username']
            user.save()
            messages.success(request, 'Buyer Registered Successfully Now Log In')
            return redirect('Shoppy:shoppy-login')
        else:
            form = BuyerSignUpForm()
            # messages.error(request, 'Form Invalid')
            # return redirect('Shoppy:shoppy-home')
            messages.error(request, 'Buyer Registration Error')
            return render(request,"shoppy/buyer-registration.html",{'form':form})
    context={

    }
    return  render(request,"shoppy/buyer-registration.html",context)


def user_login(request):
    messages = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff and user.is_active:
                login(request, user)
                return redirect('ShoppyAdmin:shoppy-admin-home')

            if user.is_active:
                if Buyer.objects.filter(user_ptr_id=user.id).exists():
                    login(request, user)
                    # if Buyer.objects.filter(user_ptr_id=user.id).exists():
                    return redirect('Shoppy:shoppy-home')
                if Seller.objects.filter(user_ptr_id=user.id).exists():
                    if Seller.objects.filter(user_ptr_id=user.id, status="VERIFIED").exists():
                        login(request, user)
                        return redirect('ShoppyAdmin:shoppy-admin-home')
                    else:
                        messages.append("It Seems That Your Account Has Been Deactivated: Contact The Admin For More Info")
                        return render(request, 'shoppy/login.html', {'errors': messages})
                # else:
                #     login(request, user)
                #     return redirect('ShoppyAdmin:shoppy-admin-home')

            else:
                messages.append('Your account has been activated!')
                return render(request, 'shoppy/login.html', {'success': messages})
        else:
            messages.append('Invalid login credentials')
            return render(request, 'shoppy/login.html', {'errors': messages})
    return render(request,"shoppy/login.html")



def logout_view(request):
    logout(request)
    return redirect('Shoppy:shoppy-login')

def seller_register(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST['username']
            user.save()
            messages.success(request, 'Seller Registered Successfully, You Will Be Notified When Your Account Is Registered')
            return redirect('Shoppy:shoppy-login')
        else:
            form = BuyerSignUpForm()
            messages.error(request,'Buyer Registration Error')
            return redirect('shoppy/seller_registration.html')


    return render(request, 'shoppy/seller_registration.html')


def seller_home(request):
    user = request.user
    seller = Seller.objects.filter(user_ptr_id=user.id).first()
    return render(request, 'shoppy_seller/sellerhome.html', {'seller':seller})

def checkout(request):
    buyer= Buyer.objects.filter(user_ptr_id= request.user.id)
    regions= Region.objects.all()
    carts = Order_Product.objects.filter(buyer_id=request.user.id)

    # print(buyer)
    context={
        'buyer':buyer,
        'regions': regions,
        'carts':carts
    }
    return render(request, 'shoppy/checkout.html', context)

def confirmCheckout(request):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    if request.method =="POST":

        form_region = request.POST['region']
        region = Region.objects.filter(id=int(form_region)).first()
        city = request.POST['city']
        phonenumber= request.POST['phonenumber']
        reference_code = get_random_string(length=9)  #allowed_chars='ACTG'

        checkout_r, created =Checkout.objects.update_or_create(
            buyer=buyer,
            region=region,
            phonenumber=phonenumber,
            city=city,
            reference_code=reference_code,
            status='VERIFIED',
        )
        if checkout_r is not None:
            checkout = Checkout.objects.filter(id=int(checkout_r.id)).first()
            # print(checkout_r)
            Order_Product.objects.filter(buyer=buyer).update(
                # checkout=checkout.id,
                checkout=checkout,
            )
            messages.success(request, 'Order Taken')
    return redirect("Shoppy:shoppy-home")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('Shoppy:shoppy-user_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request,'shoppy/user_account.html', {
        'form': form
    })

def product_sessions(request):
    username =None
    if request.method == "GET":
        if 'action' in request.GET:
            action = request.GET.get("action")














# cookies

# def setcookie(request):
#     # product =Product.objects.filter(id=product_id)
#     # response = render(request, 'shoppy/layout.html')
#     if request.method =='GET':
#         if request.session.test_cookie_worked():
#             request.session.delete_test_cookie()
#             return HttpResponse("You're logged in.")
#         else:
#             return HttpResponse("Please enable cookies and try again.")
#     request.session.set_test_cookie()
#     return render(request, 'shoppy/layout.html')





        # else:
        #     return HttpResponse("Please enable cookies and try again.")
        # request.session.response.set_cookie("product")
        # return render_to_response('shoppy/layout.html')
# def setcookie(request,product_id):
#     product = Product.objects.filter(id=product_id).first()
#     response = render(request, 'shoppy/layout.html')
#     if product:
#         if not request.COOKIES.get(product):
#             response.set_cookie('product',product_id,3600 * 24 * 365 * 2)
#         else:
#             products = request.COOKIES.get(product,product_id)+product_id
#             for product in products:
#                 response.set_cookie('product',product,3600 * 24 * 365 * 2)
#
#         return HttpResponse(response)
#     return product





















# def setcookie(request, product_id):
#     products= []
#     for product in Product.objects.all():
#         product = Product.objects.filter(id=product_id)
#         if product in request.COOKIES:
#             response = render_to_response('shoppy/layout.html',{'product':product})
#             context_instance = RequestContext(request)
#             response.set_cookie('last_connection', datetime.datetime.now())
#             response.set_cookie('user', datetime.datetime.now())
#             return response
# def getcookie(request):
#     user = request.user
#     if user in request.COOKIES and 'last_connection' in request.COOKIES:
#         user= request.COOKIES['user']
#         last_connection = request.COOKIES['last_connection']
#         last_connection_time = datetime.datetime.strptime(last_connection[:-7], "%Y-%m-%d %H:%M:%S")
#         if (datetime.datetime.now() - last_connection_time).days < 130:
#             return setcookie(request, {'user':user})
#             # return render(request, 'shoppy/layout.html', {"user": user})
#         else:
#             return render(request, 'index.html', {})
#     else:
#         return render(request, 'index.html', {})
# cookies











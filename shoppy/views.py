import msg as msg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout, login, get_user_model

from django.views.generic import View
from django.contrib.auth.models import User

from shoppy.models import *
from .forms import BuyerSignUpForm, SellerSignUpForm, BuyerUpdateForm,SellerUpdateForm,SellerLogoUpdateForm
from django.http import HttpResponse, HttpResponseNotFound, request
import datetime

# Create your views here.

def home(request):
    user = request.user
    context ={
        'title':'Shoppy-Home',
        'user': user
    }

    return render(request, 'shoppy/home.html', context)
    # return HttpResponse('<h1>shoppy home</h1>')

def productDetails(request):
    context = {
        'title': 'Shoppy-ProductDetails',
    }

    return render(request, 'shoppy/product_details.html', context)

def user_account(request):
    user = request.user
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    seller = Seller.objects.filter(user_ptr_id=user.id).first()
    print(seller)

    if buyer is not None:
        logged_in_user = 'buyer'
    elif seller is not None:
        logged_in_user = 'seller'

    b_account = BuyerUpdateForm()
    s_account = SellerUpdateForm()

    return render(request,'shoppy/user_account.html', {
        'user':logged_in_user,
        'b_account': b_account,
        's_account': s_account,
    })

def cart(request):
    context = {
        'title': 'Shoppy-Cart',
    }

    return render(request, 'shoppy/cart.html', context)

def buyer_register(request):
    if request.method == 'POST':

        form = BuyerSignUpForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Buyer Registered Successfully')
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
            print(user)
            if user.is_active:
                login(request, user)
                if Buyer.objects.filter(user_ptr_id=user.id).exists():
                    return redirect('Shoppy:shoppy-home')
                print(user)
                if Seller.objects.filter(user_ptr_id=user.id).exists():
                    return redirect('Shoppy:shoppy-seller-home')
            else:
                messages.append('Your account has been activated!')
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
            form.save()
            messages.success(request, 'Seller Registered Successfully')
            return redirect('Shoppy:shoppy-login')
        else:
            form = BuyerSignUpForm()
            messages.error(request,'Buyer Registration Error')
            return render(request,'shoppy/seller_registration.html',{'form',form})


    return render(request, 'shoppy/seller_registration.html')


def seller_home(request):
    user = request.user
    seller = Seller.objects.filter(user_ptr_id=user.id).first()
    return render(request, 'shoppy_seller/sellerhome.html', {'seller':seller})


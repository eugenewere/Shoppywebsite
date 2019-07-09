from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import BuyerSignUpForm
from django.http import HttpResponse, HttpResponseNotFound
import datetime

# Create your views here.

def home(request):
    context ={
        'title':'Shoppy-Home',
    }

    return render(request, 'shoppy/home.html', context)
    # return HttpResponse('<h1>shoppy home</h1>')

def productDetails(request):
    context = {
        'title': 'Shoppy-ProductDetails',
    }

    return render(request, 'shoppy/productdetails.html', context)

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
            return redirect('Shoppy:shoppy-home')
        else:
            form = BuyerSignUpForm()
            # messages.error(request, 'Form Invalid')
            # return redirect('Shoppy:shoppy-home')
            messages.error(request, 'Buyer Registration Error')
            return  render(request,"shoppy/buyer-registration.html",{'form':form})
    context={

    }
    return  render(request,"shoppy/buyer-registration.html",context)



from django.shortcuts import render

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
        'title': 'Shoppy-Home',
    }

    return render(request, 'shoppy/productdetails.html', context)
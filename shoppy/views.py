from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import datetime

# Create your views here.

posts =[
    {
        'author':'corey',
        'title':'Blog Post 1',
        'content':'First Post Content',
        'sutor':'corey',
        'date_posted':'August 27, 2018'
    },
    {
        'author':'eugene',
        'title':'Blog Post 2',
        'content':'First Post Content 1',
        'sutor':'corey',
        'date_posted':'August 25, 2018'
    }
]

def home(request):   
    # return render(request,"shoppy/home.html", posts)
    return HttpResponse('<h1>shoppy home</h1>')
from django.shortcuts import render, redirect, reverse
from shop.models import *

# Create your views here.
def catalog(request):
    return render(request, 'shop/comingsoon.html')
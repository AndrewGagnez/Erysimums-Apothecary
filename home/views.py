from django.shortcuts import render, redirect, reverse
from shop.models import *


'''
TODO fill this out
Purpose: 
    index below is the main page of Erysimum's Apothecary, currently it is being used as a single page application
    in that it contains all aspects of the web app / commerce site all in its home page. The most important thing 
    being the shop. For now we have views here taking from models.py that was formed in /shop and using that database
    to pull from and display product information in the shop section of the page.

Variables:
Notes:
'''
def index(request):
    products = Product.objects.all()
    return render(request, 'home/index.html', {'products':products})
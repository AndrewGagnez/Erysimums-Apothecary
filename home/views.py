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
    #TODO: tempImageWorkAround
    #tempImageWorkAround: This is a variable containing the path, /static/home/ - combined with {{product.product_image}} 
        when these two are combined they form a complete path reference to the product image which is being hosted statically,
        we cannot keep this as a permanent solution and this needs to be resolved soon(tm) via hosting media images proper via 
        Amazon S3 or some other image hosting site to properly reference product images via CDN

    #products: a reference to the products database

Notes:
'''
def index(request):
    products = Product.objects.all()
    return render(
        request, 
        'home/index.html', 
        {
            'products':products,
            'tempImageWorkAround': "/static/home/" #TODO cannot keep this as a permanent solution, need to implement external hosting for database and admin uploaded images
        }
    )
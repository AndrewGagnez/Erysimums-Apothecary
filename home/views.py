from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from shop.models import *
from django.views import View

from django.views import View

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

import datetime


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

# Create your views here.
def home(request):
    #specials = Product.objects.filter(category=Category.objects.get(name="On Sale")).values TODO reference to old method of filtering out sale items, use this as reference, delete when ready
    specials = Product.objects.filter(on_sale="True").values
    return render(
        request, 
        'index.html', 
        {
            'specials':specials,
            'tempImageWorkAround': "/static/" #TODO cannot keep this as a permanent solution, need to implement external hosting for database and admin uploaded images
        },
    
    )


class Login(View):
    return_url = None
  
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
  
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('shop:catalog')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'
  
        print(email, password)
        return render(request, 'login.html', {'error': error_message})
    
'''TODO old login account method from previous project
def login_user(request):
    if request.method == "POST":
        # Try to log in user
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        # Check if the authentication was successful
        if user is not None:
            login(request, user)
        else:
            return render(
                request,
                "login.html",
                {
                    "message": "Invalid username and/or password",
                    'Title': "Login",
                    },
                )
    
    # If it turns out user is already logged in but is trying to log in again redirect to user's homepage
    if request.method == "GET" and request.user.is_authenticated:
        return redirect(reverse("dashboard:dashboard"))

    # Just give back log in page if none of the above is true
    else:
        return render(
            request,
            "login.html",
            {
                'Title': "Login",
                },
            )
'''
  
def Logout(request):
    request.session.clear()
    return redirect('home:login')



class SignUp (View):
	def get(self, request):
		return render(request, 'signup.html')

	def post(self, request):
		postData = request.POST
		first_name = postData.get('firstname')
		last_name = postData.get('lastname')
		phone = postData.get('phone')
		email = postData.get('email')
		password = postData.get('password')
		# validation
		value = {
			'first_name': first_name,
			'last_name': last_name,
			'phone': phone,
			'email': email
		}
		error_message = None

		customer = Customer(first_name=first_name,
							last_name=last_name,
							phone=phone,
							email=email,
							password=password)
		error_message = self.validateCustomer(customer)

		if not error_message:
			print(first_name, last_name, phone, email, password)
			customer.password = make_password(customer.password)
			customer.register()
			return redirect('home:home')
		else:
			data = {
				'error': error_message,
				'values': value
			}
			return render(request, 'signup.html', data)

	def validateCustomer(self, customer):
		error_message = None
		if (not customer.first_name):
			error_message = "Please Enter your First Name !!"
		elif len(customer.first_name) < 3:
			error_message = 'First Name must be 3 char long or more'
		elif not customer.last_name:
			error_message = 'Please Enter your Last Name'
		elif len(customer.last_name) < 3:
			error_message = 'Last Name must be 3 char long or more'
		elif not customer.phone:
			error_message = 'Enter your Phone Number'
		elif len(customer.phone) < 10:
			error_message = 'Phone Number must be 10 char Long'
		elif len(customer.password) < 5:
			error_message = 'Password must be 5 char long'
		elif len(customer.email) < 5:
			error_message = 'Email must be 5 char long'
		elif customer.isExists():
			error_message = 'Email Address Already Registered..'
		# saving

		return error_message


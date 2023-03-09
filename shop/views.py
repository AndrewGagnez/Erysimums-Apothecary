from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from shop.models import *
from django.views import View
from django.views.generic import TemplateView

from paypal.standard.forms import PayPalPaymentsForm

import datetime

# Create your views here.
class Index(View):
	def post(self, request):
		product = request.POST.get('product')
		remove = request.POST.get('remove')
		cart = request.session.get('cart')
		if cart:
			quantity = cart.get(product)
			if quantity:
				if remove:
					if quantity <= 1:
						cart.pop(product)
					else:
						cart[product] = quantity-1
				else:
					cart[product] = quantity+1
  
			else:
				cart[product] = 1
		else:
			cart = {}
			cart[product] = 1
  
		request.session['cart'] = cart
		print('cart', request.session['cart'])
		return redirect('shop:catalog')
  
	def get(self, request):
		# print()
		return HttpResponseRedirect(f'/{request.get_full_path()[1:]}catalog') #TODO see what this does 
			# TODO 3/6 it seems to add a redirect! f'/get full path catalog' leads to shop/catalog when clients try to enter "websitetitle.com/shop/"


def catalog(request):
	cart = request.session.get('cart')
	if not cart:
		request.session['cart'] = {}
	products = None
	categories = Category.get_all_categories()
	categoryID = request.GET.get('category')
	if categoryID:
		products = Product.get_all_products_by_categoryid(categoryID)
	else:
		products = Product.get_all_products()
  
	data = {}
	data['products'] = products
	data['categories'] = categories
	data['tempImageWorkAround']= "/static/"
  
	print('you are : ', request.session.get('email'))
	return render(request, 'shop.html', data)



  

class Cart(View):
	def get(self , request):
		ids = list(request.session.get('cart').keys()) #TODO this line has something to do with error about 
		#looking at cart without needing to be logged in. but can we use this fact as a way to get people to checkout without logging in?
		products = Product.get_products_by_id(ids)
		print(products)
		
		#print(products.filter(product_price=1.00)) TODO useful code for future sql query shenanigans
		#print(products.values_list('product_price')) TODO useful code for future sql query shenanigans

		return render(request , 'cart.html' , 
					  {'products' : products,
					   'tempImageWorkAround': "/static/"
					   } 
					)

class CheckOut(View):
	def post(self, request):
		address = request.POST.get('address')
		phone = request.POST.get('phone')
		customer = request.session.get('customer')
		cart = request.session.get('cart')
		products = Product.get_products_by_id(list(cart.keys()))
		print(address, phone, customer, cart, products)
		
		total_price = 0
		for product in products:
			order = Order(customer=Customer(id=customer),
						product=product,
						price=product.product_price,
						address=address,
						phone=phone,
						quantity=cart.get(str(product.id)))
						#TODO model update unique identifier (order number)
						#TODO model update total price per unique identifier (order number)
						#TODO model update date of purchase
			total_price = (order.price * order.quantity) + total_price
			order.save()

			#Debugging found below
			#print(cart.get(str(product.id))) 
			#print(order.product.product_name)
			#print(order.product.product_price)

		
		product_names = [i[0] for i in list(products.values_list("product_name"))]

		

		paypal_dict = {
			"business": "sb-nbap325233031@business.example.com",
			"amount": total_price,
			"item_name": product_names,
			"invoice": "unique-invoice-id", #TODO insert unique identifier generated from order creation, here
			"notify_url": 'https://erysimums-apothecary.herokuapp.com/shop/check-out/paypal-ipn',
			"return": 'https://erysimums-apothecary.herokuapp.com/shop/cart',
			"cancel_return": 'https://erysimums-apothecary.herokuapp.com/shop/cart',
			"custom": "premium_plan",  # Custom command to correlate to some function later (optional)
		}

		# Create the instance.
		form = PayPalPaymentsForm(initial=paypal_dict)
		context = {"form": form}
		return render(request, "payment.html", context)
	
		#request.session['cart'] = {} #this clears the cart... TODO don't forget to uncomment this when PayPal is done being setup

		return redirect('shop:cart')


class OrderView(View):

	def get(self, request):
		customer = request.session.get('customer')
		orders = Order.get_orders_by_customer(customer)
		print(orders)
		return render(request, 'orders.html', {
					 'orders': orders,
					 'tempImageWorkAround': "/static/"
					}
				)
	

class PaypalReturnView(TemplateView):
    template_name = 'paypal_success.html'

class PaypalCancelView(TemplateView):
    template_name = 'paypal_cancel.html'

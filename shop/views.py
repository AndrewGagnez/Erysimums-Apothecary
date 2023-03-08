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
		ids = list(request.session.get('cart').keys())
		products = Product.get_products_by_id(ids)
		print(products)
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
		
		for product in products:
			print(cart.get(str(product.id)))
			order = Order(customer=Customer(id=customer),
						product=product,
						price=product.product_price,
						address=address,
						phone=phone,
						quantity=cart.get(str(product.id)))
			order.save()
		request.session['cart'] = {}

		paypal_dict = {
			"business": "sb-nbap325233031@business.example.com",
			"amount": "10000000.00",
			"item_name": "name of the item",
			"invoice": "unique-invoice-id",
			"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
			"return": request.build_absolute_uri(reverse('your-return-view')),
			"cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
			"custom": "premium_plan",  # Custom command to correlate to some function later (optional)
		}

		# Create the instance.
		form = PayPalPaymentsForm(initial=paypal_dict)
		context = {"form": form}
		return render(request, "payment.html", context)

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

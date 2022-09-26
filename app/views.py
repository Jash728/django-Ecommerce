from unicodedata import category
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, Category, Brand, Slider, Coupon
from .forms import  CustomerAddressForm, LoginForm, UserSignUpForm
from django.contrib import messages
from math import ceil
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import (EditProfileForm, ProfileForm)
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.db.models import Min, Max
from django.core.mail import send_mail
import socket

def error_404_view(request, exception):
	return render(request,'app/error_404.html')



def get_menu_items():
		# Fetching parent categories
		categories = [{
						'id': i.id,
						'name': i.name, 
						'pid': i.pid } for i in Category.objects.filter(pid=0).all()]

		for category in categories:

			# Fetching child cagtegory from parent category id
			sub_categories = [{
							'id': i.id, 
							'name': i.name, 
							'pid': i.pid , 
							} for i in Category.objects.filter(pid=category['id']).all()]
			category['sub_category'] = sub_categories
	
		return categories

class ProductView(View):
	def get(self, request):
		
		menu_items = get_menu_items()
		dashboard_categories = [{
								'id': i.id, 
								'name': i.name, 
								'pid': i.pid,
								'status' : i.status} 
								 for i in Category.objects.filter(is_dashboard = True).filter(~Q(pid = 0)).all()]
	   
		dashboard_category_ids = [category['id'] for category in dashboard_categories]

		dashboard_products = Product.objects.filter(is_dashboard=True).filter(category__in=dashboard_category_ids).all()
		slider_items = Slider.objects.all()
		# print("Items are ", items)

		for category in dashboard_categories:
			category['products'] = [product for product in dashboard_products if product.category.id == category['id']]
	
	   
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user = request.user))

			
		return render(request, 'app/home.html', {"totalitem" : totalitem, 
		"categories" : menu_items, "dashboard_categories" :  dashboard_categories,
		'slider_items' : slider_items})
 


class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.get(pk=pk)
		item_is_already_in_cart = False
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user = request.user))
			item_is_already_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user = request.user)).exists()
		return render(request, 'app/productdetail.html', {'product': product, 'item_is_already_in_cart' : item_is_already_in_cart, "totalitem" : totalitem})

@login_required(redirect_field_name='login')
def add_to_cart(request):
	if request.user.is_authenticated:
		
		user = request.user
		product_id = request.GET.get('prod_id')
		product = Product.objects.get(id=product_id)
		Cart(user=user, product=product).save()
		print(product_id)
		return redirect('/cart')

# for use to remove applied coupon
def remove_coupon(request, cart_id):
	cart = Cart.objects.get(id = cart_id)
	cart.coupon = None
	cart.save()
	messages.success(request, 'Coupon Removed Successfully')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# for to show the cart products
@login_required(redirect_field_name='login')
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		
		totalitem = len(Cart.objects.filter(user = request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 70.0
		total_amount = 0.0
		coupon_discount  = 0.0
		cart_product = [p for p in Cart.objects.all() if p.user == user]
		# print(cart_product)
		
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				
				if not p.coupon:
					amount += tempamount
					total_amount = amount + shipping_amount
				else:
					coupon_discount+=p.coupon.discount
					amount += tempamount
					total_amount = amount + shipping_amount - coupon_discount
				cart_obj = Cart.objects.filter(user = request.user)
				print(cart_obj)
				# print("Cart objects", cart_obj.all())	

				# For coupon code
				if request.method == 'POST':
					coupon = request.POST.get('coupon')
					
					coupon_obj = Coupon.objects.filter(code__icontains = coupon)
					print(coupon_obj[0])
				

					# if user applies wrong coupon code
					
					if not coupon_obj.exists():
						messages.warning(request, f'Invalid Coupon')
						return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

					# if user applies for more than one coupon
					cartItems = cart_obj.values_list('coupon', 'product')
					temp = list(cartItems)

					while ("" in temp):
						temp.remove("")
							
					# del temp[-1]
					
					print("list is ", temp[0])

					# for cartItem in cartItems:
						
					# 	couponDb = cartItem[4]
					# 	print(couponDb) # user e nakhyu ene e che
					# 	if couponDb==cart_obj:
					# 		print("-------------")
					# 		messages.warning(request, f'Coupon already applied')
					# 		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

						
					
						
						
					# when user total amount is less than minimum amount to apply coupon
					if total_amount < coupon_obj[0].minimum_amount:
							messages.warning(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}')
							return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

					# When applied coupon validity expired
					if coupon_obj[0].is_expired:
							messages.warning(request, f'Coupon Expired')
							return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

					Cart.objects.filter(user=request.user).update(coupon=coupon_obj[0].id)
					# print(cartItem[4])
					messages.success(request, 'Coupon applied.')
					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			
			return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount,
														   "totalitem" : totalitem, 'cart' : cart_obj})

				
		else:
			return render(request, 'app/emptycart.html')


def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity += 1
		c.save()
		amount = 0.0
	
		shipping_amount = 70.0
		cart_product = [p for p in Cart.objects.all() if p.user ==
						request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		  

		data = {
			'quantity': c.quantity,
			'amount': amount,
			'totalamount': amount + shipping_amount,
			
		}

		return JsonResponse(data)


def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity -= 1
		c.save()
		amount = 0.0
		shipping_amount = 70.0
		cart_product = [p for p in Cart.objects.all() if p.user ==
						request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		data = {
			'quantity': c.quantity,
			'amount': amount,
			'totalamount': amount + shipping_amount,
		}

		return JsonResponse(data)


def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount = 70.0
		cart_product = [p for p in Cart.objects.all() if p.user ==
						request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		data = {
			'amount': amount,
			'totalamount': amount + shipping_amount,
		}

		return JsonResponse(data)


@login_required(redirect_field_name='login')
def address(request):
	add = Customer.objects.filter(user=request.user)
	return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required(redirect_field_name='login')
def orders(request):
	user = request.user
	op = OrderPlaced.objects.filter(user = user)
	return render(request, 'app/orders.html', {'order_placed' : op})


@login_required(redirect_field_name='login')
def checkout(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user = request.user))
		user = request.user
		add = Customer.objects.filter(user=user)
		cart_items = Cart.objects.filter(user=user)
		amount = 0.0
		coupon_discount = 0.0
		shipping_amount = 70.00
		total_amount = 0.0
		cart_product = [p for p in Cart.objects.all() if p.user == user]
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				
				if not p.coupon:
					amount += tempamount
					total_amount = amount + shipping_amount
				else:
					coupon_discount+=p.coupon.discount
					amount += tempamount
					total_amount = amount + shipping_amount - coupon_discount
		return render(request, 'app/checkout.html', {'add': add, 'total_amount':total_amount, 'cart_items' : cart_items, 'totalitem' : totalitem})


@login_required(redirect_field_name='login')
def payment_done(request):
	user = request.user
	custid = request.GET.get('custid')
	customer = Customer.objects.get(id = custid)
	cart = Cart.objects.filter(user = user)
	# send_mail(
	# 	'Testing Mail',
	# 	'Here is the message',
	# 	'jsmi544068@gmail.com',
	# 	['shahjash2809@gmail.com'],
	# 	fail_silently = False
	# )

	# socket.getaddrinfo('localhost', 25)
	for c in cart:
		OrderPlaced(user = user, customer = customer, product = c.product, quantity = c.quantity, coupon = c.coupon).save()
		c.delete()
	return redirect("orders")


@login_required(redirect_field_name='login')
def profile(request):
	totalitem = 0
	totalitem = len(Cart.objects.filter(user = request.user))
	return render(request, 'app/profile.html', {'active': 'btn-primary' , 'totalitem' : totalitem})

@method_decorator(login_required, name='dispatch')
class AddressView(View):
	
	def get(self, request):
		form = CustomerAddressForm()
		return render(request, 'app/addr.html', {'form': form, 'active': 'btn-primary'})

	def post(self, request):
		form = CustomerAddressForm(request.POST)
		if form.is_valid():
			usr = request.user
			name = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality,
						   city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(
				request, 'Congratulations !! Address Added Successfully')
		return render(request, 'app/addr.html', {'form': form, 'active': 'btn-primary'})


def orderconfirmation(request):
	return render(request, 'app/order_confirmation.html')

def search(request):
	q = request.GET['search']
	data = Product.objects.filter(Q(title__icontains=q)).order_by('-id')
	# d = Brand.objects.filter(Q(name__icontains=q)).order_by('-id')
	if not data:
		return render(request, "app/itemnotfound.html")
	return render(request, 'app/search.html', {'data': data})


@login_required(redirect_field_name='login')
def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		# request.FILES is show the selected image or file
		profile_form = ProfileForm(
			request.POST, request.FILES, instance=request.user.profile)

		if form.is_valid() and profile_form.is_valid():
			user_form = form.save()
			custom_form = profile_form.save(False)
			custom_form.user = user_form
			custom_form.save()
			return redirect('profile')
		return render(request, 'app/edit_profile.html', {'form': form, 'profile_form': profile_form})
	
	else:
		form = EditProfileForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)

		return render(request, 'app/edit_profile.html', {'form': form, 'profile_form': profile_form})


def signin(request):
	if request.POST:
		form = LoginForm(request.POST)
		username = request.POST.get("username")
		password = request.POST.get("password")
		try:
			if "@" in username:
				user_object = User.objects.get(email=username)
				username = user_object.username
		except:
			pass

		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return redirect("profile")
		else:
			messages.error(request,'username or password is not correct')
			return redirect('login')
		
	else:
		form = LoginForm()

	return render(request, 'app/signin.html', {"form": form} )

class RegistrationUserView(View):
	def get(self, request):
		form = UserSignUpForm()
		return render(request, 'app/signup.html', {'form': form})

	def post(self, request):
		print(request.POST)
		form = UserSignUpForm(request.POST)
		if form.is_valid():
			messages.success(
				request, 'Congratulations!! Registered Successfully')
			form.save()
			return redirect('/registration')
		return render(request, 'app/signup.html', {'form': form})


class CatListView(ListView):
	template_name = 'app/category.html'
	context_object_name = 'catlist'
	

	def get_queryset(self):
		brand = self.request.GET.get('brand')
	   
		minMaxPrice = Product.objects.aggregate(Min('discounted_price'), Max('discounted_price'))
		

		if brand:
			products = Product.objects.filter(category__name=self.kwargs['category']).filter(brand__id=brand)
		else:
			products = Product.objects.filter(category__name=self.kwargs['category'])

		content = {
			'cat': self.kwargs['category'],
			'products': products,
			'minMaxPrice' : minMaxPrice,
		}
	   
		return content

	

		
def filter_data(request):

	# GET max and min price
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']

	# Get category from url
	urlcat = request.GET['urlcat']
	brands=request.GET.getlist('brand[]')

	# get allproducts of category which user selects
	allProducts=Product.objects.filter(category__name= urlcat).order_by('-id').distinct()
	
	# Filter cases

	# Condition for price filter
	if len(brands) == 0 :
		allProducts=allProducts.filter(discounted_price__gte=minPrice)
		allProducts=allProducts.filter(discounted_price__lte=maxPrice)	
	
	# Condition when brand filter apply and then if user removed it all the product will be shown  
	if len(brands) == 0 and (maxPrice == minPrice):
		allProducts=Product.objects.filter(category__name= urlcat).order_by('-id').distinct()
		
	# Condition for brand filter		
	if len(brands)>0 :  
		allProducts=allProducts.filter(brand__id__in=brands).distinct()  

	# Condition when both filters apply together
	if len(brands)>0 and (minPrice != maxPrice):  
		allProducts=allProducts.filter(discounted_price__gte=minPrice).filter(brand__id__in=brands).distinct()
		allProducts=allProducts.filter(discounted_price__lte=maxPrice).filter(brand__id__in=brands).distinct()	
		
   
	t=render_to_string('app/product_list.html',{'data':allProducts})
	return JsonResponse({'data':t})


def coupon_code(request):
	coupon_codes = Coupon.objects.all()
	return render(request, 'app/coupon_code.html', {'coupon_codes' : coupon_codes})

# def add_coupon(request, code)
		
# def coupon_apply(request):
# 	now = timezone.now()
# 	form = CouponApplyForm(request.POST)
# 	if form.is_valid():
# 		code = form.cleaned_data['code']
# 		try:
# 			coupon = Coupon.objects.get(code__iexact = code, valid_from__lte = now, valid_from__gte = now, active = True)
# 			request.session['coupon_id'] = coupon.id
# 		except coupon.DoesNotExist:
# 			request.session['coupon_id'] = None
	
# 	return redirect("addtocart")
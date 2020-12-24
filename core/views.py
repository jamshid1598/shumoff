from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse, BadHeaderError
from django.core import serializers
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder
from django.template import defaultfilters
from django.conf import settings
from django.db.models import F
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.db.models import Case, Value, When
from django.db.models import Q
from django.views.generic import (
	ListView,
	DetailView,
)
import json

from cart.models import (
	Customer,
	Order,
	OrderItem,
	ShippingAddress,
	OrderedItem,

	ArticleModel, 
)
from main.models import (
	New,
	Home,
	ToolVideo,
)
from cart.forms import CustomerForm
from .models import (
	Category, 
	Product, 
	Images, 
)

def cart_detail_view(request):
	data = json.loads(request.body)
	productPk = data['productPk']
	action = data['action']
	pageId = data['pageId']
	
	# print('Action:', action)
	# print('Product:', productPk)
	# print('PageId:', pageId)

	customer = request.user.customer
	print(customer)
	product = Product.objects.get(pk=productPk)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	done_action = {"added":False, "one_more":False, "already_added":False}

	if action == 'add' and pageId == "product-page" and created == True and product.quantity > orderItem.quantity:
		orderItem.quantity = (orderItem.quantity + 1)
		done_action["added"] = True
	
	elif action == 'add' and pageId == "product-page" and created == False and product.quantity > orderItem.quantity:
		done_action["already_added"] = True

	elif action == 'add' and pageId == "cart-page" and created == False and product.quantity > orderItem.quantity:
		orderItem.quantity = (orderItem.quantity + 1) 
		done_action["one_more"] = True

	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	
	orderItem.save()

	if action == 'clear':
		orderItem.delete()
	
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse(done_action, safe=False, status=200)


class HomeView(View):
	template_name='home.html'
	context={}
	
	def get_object(self):
		category_list = Category.objects.all()
		return category_list

	def get(self, request, id=None, *args, **kwargs):
		category_list = None
		category_list = self.get_object()
		
		news_img = New.objects.all()
		home_img = Home.objects.all()
		print(news_img)
		self.context["news_imgs"] = news_img
		self.context["home_imgs"] = home_img
		self.context['category_list'] = category_list

		return render(
			request,
			self.template_name,
			self.context
		)

class SearchResultsView(ListView):
	model = Product
	template_name = 'home.html'

	def get_queryset(self): # new
		query = self.request.GET.get('q')
		object_list = Product.objects.filter(
			Q(name__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query) 
		)
		return object_list
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category_list = None
		category_list = Category.objects.all()
		
		news_img = New.objects.all()
		home_img = Home.objects.all()
		context["news_imgs"] = news_img
		context["home_imgs"] = home_img
		context['category_list'] = category_list
		return context

# class CategoryDetailView(View):
# 	template_name='catalog.html'
# 	context={}

# 	def get(self, request, pk=None, *args, **kwargs):
# 		category = get_object_or_404(Category, pk=pk)
# 		category_list = Category.objects.all()
# 		self.context['category'] = category
# 		self.context['category_list'] = category_list
# 		return render(
# 			request,
# 			self.template_name,
# 			self.context
# 		)

class CategoryDetailView(View):
	template_name='catalog.html'
	context={}

	def get(self, request, pk=None, slug=None, *args, **kwargs):
		product=None
		items = None
		category = get_object_or_404(Category, pk=pk)
		category_list = Category.objects.all()

		if slug:
			product = Product.objects.get(category=category, slug=slug)
		else:
			items = category.product_category.all()
			for item in items:
				product = item
				break
			
		self.context['category'] = category
		self.context['category_list'] = category_list
		self.context["product"]=product
		return render(
		request,
		self.template_name,
		self.context
		)




class CartDetailView(View):
	template_name = 'cart.html'
	context={}
	def get(self, request, *args, **kwargs):
		# previous_path = self.request.GET.get('next', '')
		category_list = Category.objects.all()
		# print(previous_path)
		if request.user.is_authenticated:
			customer = self.request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			print("Order: ", order, '\n', "Created: ", created)
			items = order.orderitem_set.all()
		else:
			items = []
			order = {"get_cart_total": 0, "get_cart_items":0}
		self.context={
			"items":items,
			"order":order,
			# "previous_path": previous_path,
			"category_list":category_list,
		}
		return render(
			request,
			self.template_name,
			self.context,
		)



from django.core.files import File
class CheckoutDetailView(View):
	template_name = 'checkout.html'
	context={}
	def get(self, request, *args, **kwargs):
		previous_path = self.request.GET.get('next', '')
		if previous_path != "/cart/":
			previous_path = None
		category_list = Category.objects.all()
		if request.user.is_authenticated:

			customer = self.request.user.customer

			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			items = order.orderitem_set.all()
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
			items = []
			order = {"get_cart_total": 0, "get_cart_items":0}

		print("order: ", order, '\n', "items: ", items)
		self.context={
			"items":items,
			"order":order,
			"previous_path": previous_path,
			"category_list":category_list,
		}

		print("customer: ", customer)
		form=CustomerForm(instance=customer)
		self.context['form'] = form

		return render(
			request,
			self.template_name,
			self.context,
		)
	def post(self, request, *args, **kwargs):
		previous_path = self.request.POST.get('next', '')
		category_list = Category.objects.all()
		if request.user.is_authenticated:

			customer = self.request.user.customer

			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			items = order.orderitem_set.all()
			# email body format
			ordered_product_list = ""
			ordered_date = datetime.now()

			for item in items:
				ordered_product_list += f"Продукт: {item.product.name} - {item.product.price} {item.product.currency} - x{item.quantity} - {item.get_total} {item.product.currency}\n"
			ordered_product_list += f"\n\nПродукты: {order.get_cart_items}\nВсего:    {order.get_cart_total} сумма\n\nДата заказа: {ordered_date.strftime('%d/%m/%Y')}"
			# end email body format


			#  ('customer', 'product', 'product_amount', 'single_price', 'total_price', 'date_ordered', 'completed', )
			for item in items:
				ordered_item = OrderedItem.objects.create(
					customer=customer, 
					product=item.product.name,
					image = File(item.product.image),
					product_amount=item.quantity,
					single_price=item.product.price,
					total_price = item.get_total,
				)
				Product.objects.filter(slug = item.product.slug).update(quantity = F('quantity')-item.quantity)
				ordered_item.save()
				item.delete()


			# save customer order
			if request.method=="POST":
				form=CustomerForm(request.POST, instance=customer)
				if form.is_valid():
					form.save()
					
					name   	= form.cleaned_data['name']
					user    = form.cleaned_data['user']
					phone   = form.cleaned_data['phone']
					message = form.cleaned_data['message']

					print(name, user, phone, message)
					
					try:
						subject    = f"Новый заказ:"
						thoughts   = f"{name}\n{phone}\n{user}\n\n{ordered_product_list}\n\n{message}"
						sender     = settings.EMAIL_HOST_USER
						recipients = ['Javlon_Abdullaev@mail.ru', "dovurovjamshid95@gmail.com", user]
						send_mail(subject, thoughts, sender, recipients, fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header')

					return redirect('Core:customer-profile-view')
		else:
			items = []
			order = {"get_cart_total": 0, "get_cart_items":0}
		self.context={
			"items":items,
			"order":order,
			"previous_path": previous_path,
			'form': form,
			"category_list":category_list,
		}
		return render(
			request,
			self.template_name,
			self.context,
		)


class CustomerProfileView(View):
	template_name = "customer-profile.html"
	context  ={}
	def get(self, request, *args, **kwargs):
		category_list = Category.objects.all()
		if request.user.is_authenticated:
			customer = self.request.user.customer
			customer_profile = Customer.objects.get(user=self.request.user)
			ordered_items = OrderedItem.objects.filter(customer=customer)
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
			ordered_items = []
			order = {"get_cart_total": 0, "get_cart_items":0}

		self.context={
			"ordered_items":ordered_items,
			'customer':customer,
			"customer_profile":customer_profile,
			"category_list":category_list,
		}
		return render(
			request,
			self.template_name,
			self.context
		)



from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
class LazyEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return str(obj)
		return super().default(obj)

def product_detail_view(request, *args, **kwargs):
	pk = request.GET.get('request_data')
	product = Product.objects.get(pk=pk)

	if product:
		image     = product.imageURL
		images    = Images.objects.filter(model=product)
		img_dict  = {}
		img_count = 0

		for n, img in enumerate(images):
			img_dict["img"+str(n)]=img.imageURL
			img_count = n+1
		
		try:
			product_json = serializers.serialize('json', [product], cls=LazyEncoder, ensure_ascii=True)
		except Exception as e:
			print("Error occured: ", e)
		return JsonResponse({"instance": product_json, 'img_dict':img_dict, 'img_count':img_count, 'image_url': image,}, status=200)

	return Http404


def article_detail_view(request, *args, **kwargs):
	slug = request.GET.get('request_data')
	ArticleModel.objects.filter(slug = slug).update(view_counter = F('view_counter')+1)
	article = ArticleModel.objects.get(slug=slug)

	if article:
		published_date = defaultfilters.date(article.published_at, "SHORT_DATETIME_FORMAT")  #.strftime('%d/%m/%Y')
		print("date: ",published_date)
		image = article.imageURL
		try:
			article_json = serializers.serialize('json', [article], cls=LazyEncoder, ensure_ascii=True)
		except Exception as e:
			print("Error occured: ", e)
		return JsonResponse({"instance": article_json, 'image_url': image, 'published_date':published_date,}, status=200)

	return Http404


# https://dev-yakuza.posstree.com/en/django/response-model-to-json/

# https://stackoverflow.com/questions/45965610/ajax-update-variable-in-html-django

class ArticleListView(ListView):
	template_name='usefullArticle.html'
	model = ArticleModel 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["category_list"] = Category.objects.all()
		return context
	

class InstallProssecc(View):
	template_name = "blog.html"
	context = {}
	def get(self, request, *args, **kwargs):
		category_list = Category.objects.all()
		self.context["category_list"] = category_list

		videos = ToolVideo.objects.all()
		self.context["videos"] = videos

		return render(
			request, 
			self.template_name, 
			self.context
		)

class AdminControlPanel(View):
	template_name = "admincontrol.html"
	context={}
	def get(self, request, pk=None, *args, **kwargs):
		orders_in_progress = []
		orders_completed   = []
		customers          = []
		customers_list=Customer.objects.all()
		for customer in customers_list:
			exist = False
			for product in customer.customer_orders.all():
				if product and product.completed == False:
					exist = True
					break
			if exist == True:
				customers.append(customer)
			exist = False
		if self.request.user.is_superuser:
			if pk is None:
				orders_in_progress = OrderedItem.objects.filter(completed=False)
				orders_completed  = OrderedItem.objects.filter(completed=True)
			else:
				customer=Customer.objects.get(pk=pk)
				orders_in_progress = OrderedItem.objects.filter(completed=False, customer=customer)
				orders_completed  = OrderedItem.objects.filter(completed=True, customer=customer)
			print(customers)
			self.context={
					"customers" : customers,
					"orders_in_progress" : orders_in_progress,
					"orders_completed" : orders_completed,
				}
		else:
			return redirect("Core:home-view")
		self.context["category_list"] = Category.objects.all()
		return render(
			request,
			self.template_name,
			self.context,
		)

from django.db.models import Case, Value, When
def request_completed(request, *args, **kwargs):
	pk = request.GET.get('request_data')
	print(pk)
	print(OrderedItem.objects.get(pk=pk).completed)
	try:
		OrderedItem.objects.filter(pk=pk).update(completed=Case(When(completed=False, then=Value(True)),default=Value(False)))
				
	except Exception as e:
		print("Error occured: ", e)
	return JsonResponse({"instance": "Converted", }, status=200)
	

	
def request_uncompleted(request, *args, **kwargs):
	pk = request.GET.get('request_data')
	print(pk)
	print(OrderedItem.objects.get(pk=pk).completed)
	try:
		OrderedItem.objects.filter(pk=pk).update(completed=Case(When(completed=True, then=Value(False)),default=Value(True)))
		
	except Exception as e:
		print("Error occured: ", e)
	return JsonResponse({"instance": "Converted", }, status=200)





from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
class LazyEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return str(obj)
		return super().default(obj)

def accessory_tool_detail_view(request, *args, **kwargs):
	slug = request.GET.get('request_data')
	product = Product.objects.get(slug=slug)

	if product:
		image     = product.imageURL
		
		try:
			product_json = serializers.serialize('json', [product], cls=LazyEncoder, ensure_ascii=True)
		except Exception as e:
			print("Error occured: ", e)
		return JsonResponse({"instance": product_json, 'image_url': image,}, status=200)

	return Http404





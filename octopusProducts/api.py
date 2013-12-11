from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from models import Product, Recipe
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
import json
from basket_onboarding_info import Basket_onboarding_info
from basket_recommendation_engine import Basket_recommendation_engine
from django.http import HttpResponse

class ProductResource(ModelResource):
	class Meta:
		queryset = Product.objects.all()
		allowed_methods = ['get', 'post']
		resource_name = 'product'

	def prepend_urls(self):
		return [
		url(r"^(?P<resource_name>%s)/search%s$" %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('search'), name="api_product_search"),
		]

	# product/search/?format=json&term=query
	def search(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		q = request.GET.get('term', '')
		products = Product.objects.filter(name__icontains = q )[:20]

		results = []

		for product in products:
			product_json = {}
			product_json['id'] = product.id
			product_json['name'] = product.name
			product_json['price'] = product.price
			results.append(product_json)
			data = json.dumps(results)

		mimetype = 'application/json'
		return HttpResponse(data, mimetype)



class RecipeResource(ModelResource):
	class Meta:
		queryset = Recipe.objects.all()
		allowed_methods = ['get']
		resource_name = 'recipe'

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		fields = ['email', 'date_joined'] #we can either whitelist like this or blacklist using exclude
		allowed_methods = ['get', 'post']
		resource_name = 'user'
		#excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		authorization = DjangoAuthorization() #these are relevant to the API and who can access these parts of the API
		authentication = SessionAuthentication() #in other views, it would be required of us to add the "@login_required" decoration

	def prepend_urls(self):
		return [
		url(r"^(?P<resource_name>%s)/login%s$" %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('login'), name="api_login"),
		
		url(r'^(?P<resource_name>%s)/logout%s$' %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('logout'), name='api_logout'),
		
		url(r'^(?P<resource_name>%s)/signup%s$' %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('signup'), name='api_signup'),
		
		url(r'^(?P<resource_name>%s)/current%s$' %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('current'), name='api_current'),

		url(r'^(?P<resource_name>%s)/basket%s$' %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('basket'), name='api_basket'),
		]

	def login(self, request, **kwargs):
		
		self.method_check(request, allowed=['post'])
		data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

		email = data.get('email', '')
		password = data.get('password', '')

		user = authenticate(username=email, password=password)

		if user:
			if user.is_active:
				login(request, user)
				print "logged in"
				return self.create_response(request, {
					#redirect to a success page
					'success': True
					})
			else:
				return self.create_response(request, {
					'success': False,
					'reason': 'disabled',
					}, HttpForbidden )
		else:
			return self.create_response(request, {
				'success': False,
				'reason': 'incorrect',
				}, HttpUnauthorized )


	def logout(self, request, **kwargs):
		self.method_check(request, allowed=['get'])

		if request.user and request.user.is_authenticated():
			print request.user
			print request.session
			logout(request)
			return self.create_response(request, { 'success': True })
		else:
			return self.create_response(request, { 'success': False }, HttpUnauthorized)


	def signup(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

		email = data.get('email', '')
		password = data.get('password', '')

		try:
			User.objects.create_user(email, '', password)
    		
		except IntegrityError:
			print "User already exits"
			return self.create_response(request, {
				#user with same email adress already exists
				'success': False
			})
		
		# Login after registration			
		user = authenticate(username=email, password=password)
		login(request, user)

		return self.create_response(request, {
				'success': True
			})


	# Get the current user
	def current(self, request, **kwargs):
		self.method_check(request, allowed=['get'])

		if request.user.is_authenticated():
			return self.create_response(request, {
				'success': True
			})
		else:
    		# Anonymous users.
			return self.create_response(request, {
    	    	'success': False
    	    })

   	def basket(self, request, **kwargs):
   		self.method_check(request, allowed=['post'])
   		data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
   		
   		#print str(data["people"]) + " " + str(data["budget"]) + " " + str(data["cuisine"][0]) 
   		
   		# onboarding_info = Basket_onboarding_info(people = data['people'], budget = data['budget'],
   		# 	cuisines = data['cuisine'])

   		# Basket_recommendation_engine.create_onboarding_basket(onboarding_info)

   		return self.create_response(request, {
			'success': True
		})

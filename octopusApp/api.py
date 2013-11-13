from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from products.models import Product
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import Unauthorized

class ProductResource(ModelResource):
	class Meta:
		queryset = Product.objects.all()
		allowed_methods = ('get', 'post', 'put', 'delete')

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		fields = ['email']
		allowed_methods = ['get', 'post']
		resource_name = 'user'
		authorization = DjangoAuthorization()
		authentication = SessionAuthentication()

	def override_urls(self):
		return [
		url(r"^(?P<resource_name>%s)/login%s$" %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('login'), name="api_login"),
		url(r'^(?P<resource_name>%s)/logout%s$' %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('logout'), name='api_logout'),
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
		print request 
		if request.user and request.user.is_authenticated():
			print "logout"
			logout(request)
			return self.create_response(request, { 'success': True })
		else:
			print "fuck"
			return self.create_response(request, { 'success': False }, HttpUnauthorized)



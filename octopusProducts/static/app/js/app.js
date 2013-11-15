'use strict';

// Declare app level module which depends on filters, and services
angular.module('App', [
  //'ngRoute',
  'App.filters',
  'App.services',
  'App.directives',
  'App.controllers'
])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];

}])

.config(['$routeProvider', function($routeProvider) {

	$routeProvider
	.when('/home',
	{
		templateUrl: 'static/app/partials/home.html'
	})
	.when('/signup',
	{
		controller: 'RegistrationController',
		templateUrl: 'static/app/partials/signup.html'
	})
	.when('/login',
	{
		controller: 'SessionController',
		templateUrl: 'static/app/partials/login.html'
	})
	.when('/recipe',
	{
		controller: 'RecipeController',
		templateUrl: 'static/app/partials/recipe.html',
		breadcrumb: 'Recipe'
	})
	.when('/list',
	{
		controller: 'ProductListController',
		templateUrl: 'static/app/partials/product_list.html',
		breadcrumb: 'Product list'
	})
	.otherwise({ redirectTo: '/home' });
}]);

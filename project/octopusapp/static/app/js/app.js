'use strict';

// Declare app level module which depends on filters, and services
angular.module('App', [
  //'ngRoute',
  'App.filters',
  'App.services',
  'App.directives',
  'App.controllers'
])

.config(['$httpProvider','$http',function($httpProvider, $http) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

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

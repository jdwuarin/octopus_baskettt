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
	//$http.defaults.headers.post[‘X-CSRFToken’] = $cookies.csrftoken;
	//$http.defaults.headers.common[‘X-CSRFToken’] = $cookies.csrftoken;
    //$httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}])

.config(['$routeProvider', function($routeProvider) {

	$routeProvider
	.when('/home',
	{
		templateUrl: 'static/app/partials/home.html',
		requireLogin: false
	})
	.when('/signup',
	{
		controller: 'RegistrationController',
		templateUrl: 'static/app/partials/signup.html',
		requireLogin: false
	})
	.when('/login',
	{
		controller: 'SessionController',
		templateUrl: 'static/app/partials/login.html',
		requireLogin: false
	})
	.when('/recipe',
	{
		controller: 'RecipeController',
		templateUrl: 'static/app/partials/recipe.html',
		breadcrumb: 'Recipe',
		requireLogin: true
	})
	.when('/list',
	{
		controller: 'ProductListController',
		templateUrl: 'static/app/partials/product_list.html',
		breadcrumb: 'Product list',
		requireLogin: true
	})
	.otherwise({ redirectTo: '/home' });
}])

.run(['$rootScope', 'User', function($rootScope, User){

	$rootScope.$on("$routeChangeStart", function(event, currRoute, prevRoute) {
		if (currRoute.requireLogin && !User.getAuthenticated()) {
			User.redirect("/login");
		}
	});
}]);
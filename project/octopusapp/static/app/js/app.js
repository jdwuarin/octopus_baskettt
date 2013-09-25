'use strict';

var app = angular.module('App', []);

app.config(function ($routeProvider) {

	$routeProvider
	.when('/home',
	{
		templateUrl: 'static/app/partials/home.html'
	})
	.when('/products',
	{
		controller: 'ProductListController',
		templateUrl: 'static/app/partials/products.html'
	})
	.otherwise({ redirectTo: '/home' });
});

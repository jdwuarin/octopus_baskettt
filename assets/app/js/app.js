'use strict';

// Declare app level module which depends on filters, and services
angular.module('App', [
	'ngCookies',
	'ngRoute',
	'ngAnimate',
	'App.filters',
	'App.services',
	'App.directives',
	'App.controllers',
	'angulartics',
	'angulartics.google.analytics',
	'autocomplete',
	'ui.slider'
])

.config(['$httpProvider', function($httpProvider) {

    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}])

.config(['$routeProvider','$analyticsProvider', function($routeProvider,$analyticsProvider) {

	$routeProvider
	.when('/',
	{
		controller: 'HomeController',
		templateUrl: 'static/app/partials/home.html',
		requireLogin: false,
	})
	.when('/signup',
	{
		controller: 'RegistrationController',
		templateUrl: 'static/app/partials/signup.html',
		requireLogin: false
	})
	.when('/login',
	{
		controller: 'LoginController',
		templateUrl: 'static/app/partials/login.html',
		requireLogin: false
	})
	.when('/basket',
	{
		controller: 'ProductListController',
		templateUrl: 'static/app/partials/product_list.html',
		requireLogin: false
	})
	.when('/start',
	{
		controller: 'OnboardingController',
		templateUrl: 'static/app/partials/onboarding.html',
		requireLogin: false
	})
	.when('/transfer',
	{
		controller: 'TransferController',
		templateUrl: 'static/app/partials/transfer.html',
		requireLogin: true
	})
	.when('/profile',
	{
		controller: 'ProfileController',
		templateUrl: 'static/app/partials/profile.html',
		requireLogin: true
	})
	.otherwise({ redirectTo: '/' });
}])

.run(['$cookies', '$http', '$rootScope', 'User', 'Alert', '$location', function($cookies, $http, $rootScope, User, Alert,$location){

	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	$http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;

	FastClick.attach(document.body);

	$rootScope.$on("$routeChangeStart", function(event, currRoute, prevRoute) {

		// help with the margin on the product list page
		// $rootScope.productListPage = false;
		// if ($location.path() === "/basket") {
		// 	$rootScope.productListPage = true;
		// }

		// Force user to log in on required pages
		if(!User.isLoggedIn() && currRoute.requireLogin){
			User.redirect("/login");
		}

	});
}]);

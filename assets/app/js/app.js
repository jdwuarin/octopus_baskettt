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
	'angulartics.google.analytics'
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
	.when('/onboarding/:id',
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
	.otherwise({ redirectTo: '' });
}])

.run(['$cookies', '$http', '$rootScope', 'User', 'Alert', '$location', function($cookies, $http, $rootScope, User, Alert,$location){

	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	$http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;

	FastClick.attach(document.body);

	$rootScope.$on("$routeChangeStart", function(event, currRoute, prevRoute) {

		// help with the margin on the product list page
		$rootScope.productListPage = false;
		if ($location.path() === "/basket") {
			$rootScope.productListPage = true;
		}

		// Force user to log in on required pages
		if(!User.isLoggedIn()) {

			User.requestLoggedIn(function(res){
				// The user is logged in in the backend
				if(res.success){
					User.setLoggedIn(true);
				} else{
					User.setLoggedIn(false);
					if(currRoute.requireLogin){
						User.redirect("/login");
					}
				}
			});
		}


		// The onboarding process has only three steps
		if(currRoute.controller === "OnboardingController") {

			var onboarding_id = parseInt(currRoute.params.id, 10);

			if(onboarding_id === 0 || onboarding_id > 2) {
				User.redirect("/");
			}

		}
	});
}]);

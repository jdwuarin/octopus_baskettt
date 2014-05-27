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
	'ui.slider'
]);

angular.module('App.controllers', [
	'ngSanitize',
	'ui.bootstrap'
]);

angular.module('App.services', [
	'LocalStorageModule'
]);

angular.module('App.directives', []);
angular.module('App.filters', []);


angular.module('App')

.config(['$httpProvider', '$parseProvider', function($httpProvider, $parseProvider) {

    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];

    $parseProvider.unwrapPromises(true);
}])

.config(['$routeProvider','$analyticsProvider', function($routeProvider,$analyticsProvider) {

	$routeProvider
	.when('/',
	{
		controller: 'RegistrationController',
		templateUrl: 'static/app/partials/signup.html',
		requireLogin: false,
	})
	.when('/reset',
	{
		controller: 'ResetController',
		templateUrl: 'static/app/partials/reset.html'
	})
	.when('/reset/:uidb64/:token',
	{
		controller: 'ResetConfirmController',
		templateUrl: 'static/app/partials/reset_confirm.html'
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
	.when('/baskets/create',
	{
		controller: 'BasketsCreateController',
		templateUrl: 'static/app/partials/baskets_create.html',
		requireLogin: true,
		showOnly: false,
	})
	.when('/baskets/:slug',
	{
		controller: 'BasketsCreateController',
		templateUrl: 'static/app/partials/baskets_create.html',
		requireLogin: false,
		showOnly: true,
	})
	// .when('/start',
	// {
	// 	controller: 'OnboardingController',
	// 	templateUrl: 'static/app/partials/onboarding.html',
	// 	requireLogin: false
	// })
	.when('/profile',
	{
		controller: 'ProfileController',
		templateUrl: 'static/app/partials/profile.html',
		requireLogin: true
	})
	// .when('/profile/basket',
	// {
	// 	controller: 'ProfileBasketController',
	// 	templateUrl: 'static/app/partials/profile_basket.html',
	// 	requireLogin: true
	// })
	.otherwise({ redirectTo: '/' });
}])

.run(['$cookies', '$http', '$rootScope', 'User', 'Alert', '$location', function($cookies, $http, $rootScope, User, Alert,$location){

	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	$http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;

	FastClick.attach(document.body);

	$rootScope.$on("$routeChangeStart", function(event, currRoute, prevRoute) {

		var location = $location.path();

		// No homepage and onboarding when loggedin
		if(User.isLoggedIn() && (currRoute === "/start" || currRoute === "/")){
			User.redirect("baskets/create");
		}

		// Force user to log in on required pages
		if(!User.isLoggedIn() && currRoute.requireLogin){
			User.redirect("/login");
		}


		$rootScope.showOnly = false;

		if(!angular.isUndefined(currRoute.showOnly) && currRoute.showOnly){
			$rootScope.showOnly = true;
			$('body').addClass('hide-search');
		} else {
			$('body').removeClass('hide-search');
		}

	});
}]);

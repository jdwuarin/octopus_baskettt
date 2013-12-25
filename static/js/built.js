'use strict';

// Declare app level module which depends on filters, and services
angular.module('App', [
	'ngCookies',
	'ngRoute',
	'App.filters',
	'App.services',
	'App.directives',
	'App.controllers'
])

.config(['$httpProvider', function($httpProvider) {

    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}])

.config(['$routeProvider', function($routeProvider) {

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

.run(['$cookies', '$http', '$rootScope', 'User', function($cookies, $http, $rootScope, User){
	
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	$http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;

	$rootScope.$on("$routeChangeStart", function(event, currRoute, prevRoute) {

		if(!User.isLoggedIn()) {

			User.requestLoggedIn(function(res){
				// The user is logged in in the backend
				if(res.success){
					User.setLoggedIn(true);
				}

				else{
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

			if(onboarding_id === 0 || onboarding_id > 3) {
				User.redirect("/");
			}

		}
	});
}]);;'use strict';

/* Controllers */

angular.module('App.controllers', ['ngSanitize','ui.bootstrap'])

	.controller('OnboardingController', ['$scope', '$routeParams', 'Preference', function($scope, $routeParams, Preference) {

		$scope.cuisines = [{ "name": "Italian", "image": "italian.png"},
		{ "name": "Chinese", "image": "chinese.png"},
		{ "name": "Indian", "image": "indian.png"},
		{ "name": "Spanish", "image": "spanish.png"},
		{ "name": "Thai",  "image": "thai.png"},
		{ "name": "French",  "image": "french.png"}];

		$scope.preference = {};

		var page_id = parseInt($routeParams.id,10);

		$scope.page = page_id;


		$scope.saveData = function() {
			if(page_id === 2) {
				Preference.setPeople($scope.preference.people);
			} else if (page_id === 3) {
				Preference.setBudget($scope.preference.budget);
			}
		};

		$scope.isActive = function(id) {
			return id === page_id;
		};

		$scope.getNextPage = function() {
			// The onboarding process only has 3 steps
			if(page_id < 3 && page_id > 0) {
				return "#/onboarding/" + (page_id+1).toString();
			// When you're done with the onboarding you're transfered to the product list
			} else if(page_id === 3) {
				return "#/basket";
			// Edge case
			} else {
				return "#/";
			}
		};


	}])

	.controller('ProductListController', ['$rootScope','$scope','Preference','Basket', 'Product', 'User',function($rootScope, $scope, Preference, Basket, Product, User) {

		var preferenceList = Preference.getAll();
		$scope.user = {};

		$rootScope.$on('CloseSignUpForm', function(){
			$scope.closeForm();
		});
		
		Basket.post(preferenceList, function(res){
			$scope.products = res;
		});

		$scope.resetSelection = function(){
			$scope.$broadcast('resetSelection');
		};

		$scope.searchProducts = function(){
			Product.search($scope.queryTerm, function(res){
				$scope.search_result = res;
			});
		};

		$scope.transferBasket = function(){
			if(!User.isLoggedIn()) {
				$scope.toggleForm(true);
			}
		};

		$scope.closeForm = function() {
			$scope.toggleForm(false);
		};

		$scope.signup = function(){
			var user = $scope.user;
			if($scope.signupForm.$valid){

				User.signup(user.email, user.password, function(data){
					$rootScope.$emit('UserSignedUp');
				});
			}
		};

	}])

	.controller('RegistrationController', ['$scope','User', function($scope,User) {

		$scope.user = {};

		$scope.signup = function(){
			var user = $scope.user;
			if($scope.signupForm.$valid){

				User.signup(user.email, user.password, function(data){
					// This callback is only called when return success
					User.redirect("/");
				});
			}
		};
	}])

	.controller('LoginController', ['$sanitize','$scope','User','Alert', function($sanitize,$scope,User,Alert) {
		$scope.user = {};

		var sanitizeCredentials = function(credentials) {
			return {
				email: $sanitize(credentials.email),
				password: $sanitize(credentials.password)
			};
		};

		$scope.login = function(){
			var user = $scope.user;
			if($scope.loginForm.$valid){
				user = sanitizeCredentials(user);

				User.login(user.email, user.password, function(data){
					User.setLoggedIn(true);
					Alert.add("Successfully logged in.", "success")
					User.redirect("/");
				});
			}
		};

	}])

	.controller('AlertController', ['$scope', 'Alert', function($scope, Alert) {

		$scope.alerts = Alert.getAll();

		$scope.closeAlert = function(index) {
			Alert.close(index);
			$scope.alerts = Alert.getAll();
		};

	}]);
;'use strict';

/* Directives */


angular.module('App.directives', [])

	// When you click on the DOM a the .selected class is injected
	.directive('click', ['Preference',function(Preference) {
		return function(scope, element, attrs) {

			//Initialize the status
			var selected_preference = Preference.getCuisine();

			var selected = selected_preference.some(function(el){
				return scope.cuisine.name === el;
			});

			scope.selectedStatus = selected;
			
			element.bind("click", function() {

				scope.selectedStatus = !scope.selectedStatus;
				Preference.setCuisine(scope);
				scope.$apply();
			});
		};
	}])

	.directive('signup',[function() {
		return {
			link: function (scope, element, attrs) {
				scope.isVisible = false;
				scope.toggleForm = function(value){
					scope.isVisible = value;
				};
			},
			restrict: 'E',
			templateUrl: 'static/app/partials/_sign_up.html'
		};
	}])

	.directive('navbar',['$rootScope', 'User', function($rootScope, User) {

		return {
			link: function (scope, element, attrs) {

				$rootScope.$on('UserSignedUp', function(){
					User.requestLoggedIn(function(res){
						if(res.success){
							User.setLoggedIn(true);
							scope.userIsLoggedIn();
							$rootScope.$emit('CloseSignUpForm');
						}
					});
				});

				scope.userIsLoggedIn = function(){
					// Defined as a function to force the execution after a redirection
					return User.isLoggedIn();
				};

				scope.logout = function(){
					User.logout(function(data){
						User.setLoggedIn(false);
						// This callback is only called when return success
						User.redirect("/");
					});
				};
			},
			restrict: 'E',
			templateUrl: 'static/app/partials/_nav_bar.html'
		};
	}])

	.directive('remove', [function() {

		return {
			link: function (scope, element, attrs) {
				scope.$on('resetSelection', function() {
					scope.selectedStatus = false;
				});

				element.bind("click", function() {
					scope.selectedStatus = !scope.selectedStatus;
					scope.$apply();
				});
			},
			template: '<i class="glyphicon glyphicon-remove"></i>',
			transclude: true
		};
		
	}]);
;'use strict';

/* Filters */

angular.module('App.filters', []).
filter('filteredrecipes', [function() {
	return function(recipes,diets){
		if(recipes === undefined)
			return;
		
		var result = recipes.slice();// copy array
		var recipe; 

		angular.forEach(diets, function(value, key) { //Checks if the keyword is in the title
			if(value) {
				for(var index = 0; index < result.length; index++) {
					recipe = result[index];
					if(recipe.title.indexOf(key) == -1) {
						result.splice(index--,1);
					}
				}
			}
		});
		return result;
	};
}]);;'use strict';

/* Services */

angular.module('App.services', ['LocalStorageModule'])

	// Factory that uses the REST api/v1
	.factory('Product', ['$http', function($http) {

		function getUrl(id) {
			id = typeof id !== 'undefined' ? id : ''; //if no id put empty string i.e. for get all products
			return 'http://127.0.0.1:8000/api/v1/product/' + id + '?format=json';
		}

		return {
			get: function(id, callback) { // GET /id
				return $http.get(getUrl(id)).success(callback);
			},
			query: function(callback) { // GET /
				return $http.get(getUrl()).success(callback);
			},
			save:function(product,callback) {
				return $http.post(getUrl(), product).success(callback);
			},
			remove: function(id, callback) {
				return $http.delete(getUrl(id)).success(callback);
			},
			put: function(product, callback) {
				return $http.put(getUrl(product.id), product).success(callback);
			},
			search: function(term, callback) {
				return $http.get(getUrl("search/") + "&term=" + term).success(callback);
			}
		};
	}])

	// Factory that uses our user api
	.factory('User', ['$cookies', '$http', '$location', function($cookies, $http, $location) {

		function getUrl(req) {
			return 'http://127.0.0.1:8000/api/v1/user/' + req + '/?format=json';
		}

		var LoggedIn = null;

		return {
			login: function(email, password, callback) { // POST /user/login
				return $http({
					url: getUrl('login'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback);
			},
			logout: function(callback) { // GET /user/logout
				return $http({
					url: getUrl('logout'),
					method: "GET"
				}).success(callback);
			},
			redirect: function(url){
				// Redirect to the given url (defaults to '/')
				url = url || '/';
				$location.path(url);
			},
			isLoggedIn: function() {
				return LoggedIn;
			},
			setLoggedIn: function(val) {
				LoggedIn = val;
			},
			signup: function(email, password, callback) {
				return $http({
					url: getUrl('signup'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback);
			},
			// Check if logged in in Django backend
			// Avoid losing a session when a user reloads the page
			requestLoggedIn: function(callback) {
				return $http({
					url: 'http://127.0.0.1:8000/api/v1/user/current/?format=json',
					method: "GET",
					headers: {'Content-Type': 'application/json'},
				}).success(callback);
			}
		};
	}])

	// Service that contains the preferences in the onboarding
	.service('Preference', [function() {

		var preferenceList = {};
		preferenceList.cuisine= [];

		return {
			getCuisine: function() {
				return preferenceList.cuisine;
			},
			setCuisine: function(scope) {

				var isPresent = false;
				
				for (var i = preferenceList.cuisine.length-1; i >= 0; i--) {

						if (preferenceList.cuisine[i] == scope.cuisine.name) { //if it's in the list
							isPresent = true;

							if(!scope.selectedStatus){
								preferenceList.cuisine.splice(i,1);
							}
						}
				}

				if (!isPresent && scope.selectedStatus) {
					preferenceList.cuisine.push(scope.cuisine.name);
				}
			},
			setPeople: function(count) {
				preferenceList.people = count;
			},
			setBudget: function(amount) {
				preferenceList.budget = amount;
			},
			getAll: function() {
				return preferenceList;
			}
		};
	}])


	// Factory that uses that keeps the data during the onboarding
	.factory('localStorage',  ['localStorageService', function(localStorageService) {

		return {
			add: function(key, value) {
				localStorageService.add(key, value);
			},

			get: function(key) {
				return localStorageService.get(key);
			}
		};

	}])

	.factory('Basket',  ['$http', function($http) {

		return {
			post: function(list, callback) {
				return $http.get('static/app/js/product.json').success(callback);
				// return $http({
				// 	url: 'http://127.0.0.1:8000/api/v1/user/basket/?format=json',
				// 	method: "POST",
				// 	headers: {'Content-Type': 'application/json'},
				// 	data: list
				// })
			}
		};

	}])

	.factory('Alert',  [function() {
		
		var alertList = [];

		return {
			add: function(message, type) {
				alertList.push({msg: message, type: type});
			},
			close: function(index) {
				alertList.splice(index, 1);
			},
			getAll: function() {
				return alertList;
			}
		};

	}]);

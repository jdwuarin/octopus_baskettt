'use strict';

/* Controllers */

angular.module('App.controllers', ['ngSanitize'])

	.controller('HomeController', ['$scope', function($scope) {

	}])

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

	.controller('IngredientController', ['$scope','$http','Product',function($scope, $http, Product) {

		$scope.diets = {};
		$scope.cart = {};

		Product.query(function(res) {
			$scope.products = res.objects;
		});

	}])

	.controller('ProductListController', ['$scope','Preference','Basket', 'Product',function($scope, Preference, Basket, Product) {
		var preferenceList = Preference.getAll();

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
		}
	}])

	.controller('LoginController', ['$sanitize','$scope','User', function($sanitize,$scope,User) {
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
					// This callback is only called when return success
					User.redirect("/");
				});
			}
		}

	}])

	.controller('NavigationController', ['$cookieStore', '$scope','User', function($cookieStore,$scope,User) {

		$scope.userIsLoggedIn = function(){
			// Defined as a function to force the execution after a redirection
			return User.isLoggedIn();
		}

		$scope.logout = function(){
			User.logout(function(data){
				User.setLoggedIn(false);
				// This callback is only called when return success
				User.redirect("/");
			});
		}
	}]);

'use strict';

/* Controllers */

angular.module('App.controllers', ['ngSanitize'])

	.controller('HomeController', ['$scope', function($scope) {

	}])

	.controller('OnboardingController', ['$scope', '$routeParams', function($scope, $routeParams) {
		$scope.cuisines = [{ "name": "Italian"},
		{ "name": "Chinese"},
		{ "name": "Indian"},
		{ "name": "Spanish"},
		{ "name": "Thai"},
		{ "name": "French"}];


		var page_id = parseInt($routeParams.id);

		$scope.page = page_id;
		
		$scope.isActive = function(id) {
			return id === page_id;
		};

		$scope.getNextPage = function() {
			// The onboarding process only has 3 steps
			if(page_id < 3 && page_id > 0) {
				return "#/onboarding/" + (page_id+1).toString();
			// When you're done with the onboarding you're transfered to the product list
			} else if(page_id === 3) {
				return "#/list";
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

	.controller('ProductListController', ['$scope','$http','Product','Recommendation',function($scope, $http, Product,Recommendation) {

		//var selectedRecipesIds = selectedRecipes.getObjects();

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

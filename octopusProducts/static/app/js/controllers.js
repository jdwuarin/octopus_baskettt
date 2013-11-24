'use strict';

/* Controllers */

angular.module('App.controllers', [])
	
	.controller('RecipeController', ['$scope','$http','Recipe','selectedRecipes',function($scope, $http, Recipe, selectedRecipes) {

		// Recipe.query(function(data) {
		// 	$scope.recipes = data.items;
		// });

		$scope.diets = {};

	}])
	.controller('ProductListController', ['$scope','$http','Product','selectedRecipes','Recommendation',function($scope, $http, Product, selectedRecipes,Recommendation) {

		var selectedRecipesIds = selectedRecipes.getObjects();

		// Recommendation.post(selectedRecipesIds,function(data) {
		// $scope.products = data.objects;
		// });
	}])

	.controller('RegistrationController', ['$scope','User', function($scope,User) {

		$scope.user = {};

		$scope.signup = function(){
			var user = $scope.user;
			if($scope.signupForm.$valid){
				console.log(user.email);
				console.log(user.password);

				User.signup(user.email, user.password, function(data){
					// This callback is only called when return success
					User.redirect("/");
				});
			}
		}
	}])

	.controller('LoginController', ['$scope','User', function($scope,User) {
		$scope.user = {};
		
		$scope.login = function(){
			var user = $scope.user;
			if($scope.loginForm.$valid){
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
			// Defined as a function to force the execution after a redirectio
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

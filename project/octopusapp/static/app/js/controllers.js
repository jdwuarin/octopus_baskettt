'use strict';

/* Controllers */

angular.module('App.controllers', [])
	
	.controller('RecipeController', ['$scope','$http','Recipe','selectedRecipes',function($scope, $http, Recipe, selectedRecipes) {

		Recipe.query(function(data) {
			$scope.recipes = data.items;
		});
		// Product.query(function(data) {
		// 	$scope.recipes = data.objects;
		// });

		$scope.diets = {};

	}])
	.controller('ProductListController', ['$scope','$http','Product','selectedRecipes','Recommendation',function($scope, $http, Product, selectedRecipes,Recommendation) {

		// Product.query(function(data) {
		// 	$scope.products = data.objects;
		// });
		var selectedRecipesIds = selectedRecipes.getObjects();

		Recommendation.post(selectedRecipesIds,function(data) {
			$scope.products = data.objects;
		});
		
	}])
	.controller('RegistrationController', ['$scope','User', function($scope,User) {

		User.login(function(data){
			console.log(data);
			console.log("putain");
		});

		$scope.user = {};

		$scope.signUp = function(){
			var user = $scope.user;
			console.log(user);
			console.log($scope.signUpForm);
			if($scope.signUpForm.$valid){
				alert("OK");
			}
		}

	}])
	.controller('StatusController', ['$scope','$location',function($scope, $location) {

		$scope.isActive = function(route) {
			return route === $location.path();
		}

	}]);
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
	.controller('StatusController', ['$scope','$location',function($scope, $location) {

		$scope.isActive = function(route) {
			return route === $location.path();
		}

	}]);
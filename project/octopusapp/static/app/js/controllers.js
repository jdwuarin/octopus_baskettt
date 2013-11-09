'use strict';

/* Controllers */

angular.module('App.controllers', [])
	
	.controller('RecipeController', ['$scope','$http','Recipe','selectedRecipes',function($scope, $http, Recipe, selectedRecipes) {

		Recipe.query(function(data) {
			$scope.recipes = data.items;
		});

		$scope.diets = {};

        selectedRecipes.setObjects("Chicken");

	}])
	.controller('ProductListController', ['$scope','$http','Product','selectedRecipes',function($scope, $http, Product, selectedRecipes) {

		Product.query(function(data) {
			$scope.products = data.objects;
		});

	}])
	.controller('StatusController', ['$scope','$location',function($scope, $location) {

		$scope.isActive = function(route) {
			return route === $location.path();
		}

	}]);
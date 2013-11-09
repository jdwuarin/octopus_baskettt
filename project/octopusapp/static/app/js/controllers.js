'use strict';

/* Controllers */

angular.module('App.controllers', [])
	
	.controller('RecipeController', ['$scope','$http','Recipe',function($scope, $http, Recipe) {

		Recipe.query(function(data) {
			$scope.recipes = data.items;
		});

		$scope.diets = {};

	}])
	.controller('ProductListController', ['$scope','$http','Product',function($scope, $http, Product) {

		Product.query(function(data) {
			$scope.products = data.objects;
		});

	}])
	.controller('StatusController', ['$scope','$location',function($scope, $location) {
		
		$scope.status = {

		};

		$scope.isActive = function(route) {
			return route === $location.path();
		}

	}]);
'use strict';

/* Controllers */

angular.module('App.controllers', []).
	controller('RecipeController', ['$scope','$http','Product','Recipe',function($scope, $http, Product, Recipe) {

		Product.query(function(data) {
			$scope.products = data.objects;
		});

		Recipe.query(function(data) {
			$scope.recipes = data.items;
		});

		$scope.diets = {};

	}]);




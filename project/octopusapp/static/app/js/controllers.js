'use strict';

/* Controllers */

angular.module('App.controllers', []).
	controller('RecipeController', ['$scope','$http',function($scope, $http) {

		$scope.url = "http://baskettt.apiary.io"; // To change later to our own API

		$scope.getRecipes = function() {
			$http.get($scope.url + '/recipes').
			success(function(data) {
				$scope.recipes = data.items;
			});
		};

		$scope.getRecipes();

		$scope.diets = {};

	}]);




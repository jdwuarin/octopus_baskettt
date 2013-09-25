'use strict';

app.controller('ProductListController', function($scope, $http) {

	$scope.url = "http://baskettt.apiary.io"; // To change later to our own API

	$scope.getIndex = function() {
		$http.get($scope.url + '/products').
		success(function(data) {
			$scope.products = data.items;
		});
	};

	$scope.getIndex();	

});
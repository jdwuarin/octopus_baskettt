angular.module('App.controllers').controller('ProfileController',
	['$scope','User','Alert', 'Basket',
	function($scope, User, Alert, Basket){

	$scope.email = User.email();

	Basket.fetchAll().then(function(res){
		$scope.baskets = res.data;
	});

}]);

angular.module('App.controllers').controller('AlertController',
	['$scope', 'Alert', '$timeout', '$location',
	function($scope, Alert, $timeout, $location) {

	$scope.alerts = Alert.getAll();

	$scope.closeAlert = function(index) {
		Alert.close(index);
		$scope.alerts = Alert.getAll();
	};

}]);

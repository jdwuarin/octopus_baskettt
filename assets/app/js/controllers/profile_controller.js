angular.module('App.controllers').controller('ProfileController',
	['$scope','User','Alert', 'Basket',
	function($scope, User, Alert, Basket){

	$scope.email = User.email();

	Basket.fetchAll().then(function(res){
		$scope.baskets = res.data;
	});

	User.getSettings(function(res){
		$scope.email = res.email;
		$scope.recommendationEmailSubscription = res.recommendation_email_subscription;
		$scope.newsEmailSubscription = res.news_email_subscription;
	});

	$scope.updateInfos = function() {
		if($scope.settingsForm.$valid && $scope.email.length > 0) {
			User.updateInfos(
				$scope.email,
				$scope.recommendationEmailSubscription,
				$scope.newsEmailSubscription,
				function(res){
					if(res.success){
						Alert.add("Your settings have been updated.","success");
					} else{
						Alert.add(res.message,"danger");
					}
				});
		}
	};
}]);

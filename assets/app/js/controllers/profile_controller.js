angular.module('App.controllers').controller('ProfileController',
	['$scope','User','Alert',
	function($scope, User,Alert){

	$scope.email = User.email();

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

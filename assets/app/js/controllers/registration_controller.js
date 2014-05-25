angular.module('App.controllers').controller('RegistrationController',
	['$scope','User','Alert',
	function($scope,User,Alert) {

	$scope.user = {};

	$scope.signup = function(){
		var user = $scope.user;
		if($scope.signupForm.$valid){

			User.signup(user.email, user.password, function(data){
				// This callback is only called when return success
				// User.redirect("/");
				if(data.reason == "not_invited"){
					Alert.add("You haven't been invited to the beta. You'll get an invite in your inbox in the next few weeks.", "info");
				} else if(data.reason == "already_exist"){
					Alert.add("You already have an account associated with this email address.", "info");
				}
			},function(res, status){
				if(status == 401){
					Alert.add("You haven't been authorized to use the beta. Stay tuned!", "info");
				}
			});
		}
	};
}]);

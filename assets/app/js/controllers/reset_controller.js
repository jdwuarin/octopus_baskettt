angular.module('App.controllers').controller('ResetController', ['$scope', '$http', 'Alert', 'User', function($scope, $http, Alert, User){

	$scope.email = "";

	$scope.passwordReset = function() {
		if($scope.passwordResetForm.$valid){
			User.resetPasswordEmail($scope.email, function(res){
				if(res.status === "mail_sent") {
					Alert.add("Check your email inbox for the reset password link.","success");
				}
			});
		}
	};


}]);



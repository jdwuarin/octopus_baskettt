angular.module('App.controllers').controller('ResetConfirmController',
	['$scope', '$routeParams', 'User', '$http', 'Alert',
	function($scope, $routeParams, User, $http, Alert){

	var token = $routeParams.token,
	uidb64 = $routeParams.uidb64;

	if(!!token && !!uidb64){
		$scope.sendNewPassword = function() {
			User.resetPasswordConfirm(uidb64, token, $scope.password1, $scope.password2, function(res){

				if (res.reason === "password_mismatch"){
					Alert.add("Please try again, passwords don't match.","danger");
				} else if (res.reason === "password_too_short"){
					Alert.add("Please enter a password with at least 8 characters.","danger");
				} else if(res.status === "success"){
					Alert.add("Your password has been reset.","success");
				} else{
					Alert.add("This link has already been used.","danger");
				}
			});
		};
	} else {
		User.redirect("/reset");
	}

}]);

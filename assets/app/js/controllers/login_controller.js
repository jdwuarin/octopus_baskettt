angular.module('App.controllers').controller('LoginController',
	['$sanitize','$scope','User','Alert',

	function($sanitize,$scope,User,Alert) {
	$scope.user = {};

	var sanitizeCredentials = function(credentials) {
		return {
			email: $sanitize(credentials.email),
			password: $sanitize(credentials.password)
		};
	};

	$scope.login = function(){
		var user = $scope.user;
		if($scope.loginForm.$valid){
			user = sanitizeCredentials(user);

			User.login(user.email, user.password,
				function(data){
					User.setLoggedIn(true);
					User.redirect("/basket");
				},function(res, status){
					Alert.add("Wrong credentials.", "danger");
				});
		}
	};

}]);

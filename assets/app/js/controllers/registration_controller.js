angular.module('App.controllers').controller('RegistrationController',
	['$scope','User','Alert',
	function($scope,User,Alert) {

	$scope.user = {};

	$scope.signup = function(){
		var user = $scope.user;

		if(user.password !== user.passwordConfirmation){
			return Alert.add("Passwords don't match", 'danger');
		}

		User.signup(user.email, user.password, user.passwordConfirmation).then(function(res){
			if(res.data.success === false){
				if(res.data.reason === "already_exists") return Alert.add('This email address is already registered', 'danger');
				else return Alert.add('Something went wrong', 'danger');
			} else {

				if(!User.isLoggedIn()) {
					User.requestLoggedIn(function(res){
						// The user is logged in in the backend
						if(res.success){
							User.setLoggedIn(true);
							User.redirect('/baskets/create');
						} else{
							User.setLoggedIn(false);
						}
					});
				}
			}
		});
	};

}]);

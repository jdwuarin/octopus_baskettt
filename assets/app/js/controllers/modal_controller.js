angular.module('App.controllers').controller('ModalCtrl',
	['$scope', '$modalInstance', 'products','User','$sanitize','Basket','Preference','Tesco', '$analytics',
	function($scope, $modalInstance, products, User, $sanitize,Basket,Preference,Tesco,$analytics){

		$scope.tescoCredential = {};
		$scope.user = {};
		$scope.unsuccessfulItems = [];

		$scope.signup = true; // shows sign up at first
		$scope.sendTescoForm = true;
		$scope.loggedin = false;
		$scope.notInvited = false;
		$scope.good_login = true;

		$scope.errorMessage = "";
		$scope.toggleError = $scope.errorMessage.length > 0;


		if(User.isLoggedIn()){
			$scope.loggedin = true;
		}

		var sanitizeCredentials = function(credentials) {
			return {
				email: $sanitize(credentials.email),
				password: $sanitize(credentials.password)
			};
		};

		$scope.signup = function(){
			var user = $scope.user,
			user_settings_hash = Basket.getUserSettingsKey();

			if(typeof user_settings_hash === "undefined") {
				user_settings_hash = "";
			}

			if(user.password !== user.passwordConfirmation){
				$scope.errorMessage = "Passwords don't match.";
				return;
			}

			User.signup(user.email, user.password, user.passwordConfirmation, user_settings_hash, function(res){
				if(res.success === false){
					$scope.toggleError = true;
					if(res.reason === "already_exists"){
						$scope.errorMessage = "An accont using this email already exists.";
					} else if (res.reason === "password_mismatch"){
						$scope.errorMessage = "Passwords don't match.";
					} else if (res.reason === "password_too_short"){
						$scope.errorMessage = "Please enter a password with at least 8 characters.";
					} else if (res.reason ==="not_accepted"){
						$scope.errorMessage = "Your account isn't ready yet. We will inform you when you will have access to the baskettt goodness.";
					} else if (res.reason ==="not_invited"){
						$scope.errorMessage = "You haven't been invited to the beta. We have added you to our list and will inform you when your account is ready";
					} else if (res.reason ==="user_settings_not_found"){
						$scope.errorMessage = "It seems you took more than 2 weeks to create your basket. We're sorry about that, but you will need to start again from the start";
					} else{
						$scope.errorMessage = "Something went wrong on our end. Please try again";
					}
				} else {
					$scope.toggleError = false;

					if(!User.isLoggedIn()) {
						User.requestLoggedIn(function(res){
							// The user is logged in in the backend
							if(res.success){
								User.setLoggedIn(true);
								$scope.loggedin = true;
							} else{
								User.setLoggedIn(false);
							}
						});
					}
				}
			});
		};

		$scope.login = function(){
			var user = $scope.user;
			user = sanitizeCredentials(user);
			User.login(user.email, user.password, function(data){
				User.setLoggedIn(true);
				$scope.loggedin = true;
			});
		};

		$scope.sendToTesco = function(){
			var tescoCredential = $scope.tescoCredential,
			list = products;

			var oldRecommendation = Basket.getOldRecommendation(),
			preference = Preference.getAll(),
			user_settings_hash = Basket.getUserSettingsKey(),
			recommended_basket_id = Basket.getRecommendedBasketId();

			$analytics.eventTrack('ClickToSend',
				{  category: 'BasketPorting'});

			$scope.loading = true;
			$scope.sendTescoForm = false;

			if(list.length === 0 || list === undefined){ return; }

			Tesco.post(tescoCredential.email,
				tescoCredential.password,
				list,
				oldRecommendation,
				preference,
				user_settings_hash,
				recommended_basket_id,
				function(res) {
					$scope.loading = false;

					if(res.good_login === "False") {
						$scope.errorMessage = "Wrong Tesco credentials.";
						$scope.sendTescoForm = true;
						$scope.toggleError = true;
					} else if(res.server_timeout === "True"){
						$scope.errorMessage = "Something went wrong on our side. Please retry in a few minutes.";
						$scope.sendTescoForm = true;
						$scope.toggleError = true;
					} else {
						var unsuccessfulItems = Tesco.getUnsuccessful(res);
						Basket.clearLocal();
						if(unsuccessfulItems.length === 0){
							$analytics.eventTrack('SuccessfullyTransfered',
								{  category: 'BasketPorting'});
							$scope.unsuccessfulTransfer = false;
							Basket.addLocal([]);
						} else{
							$analytics.eventTrack('UnsuccessfullyTransfered',
								{  category: 'BasketPorting'});
							$scope.unsuccessfulTransfer = true;
							$scope.unsuccessfulItems = unsuccessfulItems;
						}
					}
				});
		};

	}]);

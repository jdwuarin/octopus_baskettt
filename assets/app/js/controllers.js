'use strict';

/* Controllers */

angular.module('App.controllers', ['ngSanitize','ui.bootstrap'])

.controller('ResetController', ['$scope', '$http', 'Alert', 'User', function($scope, $http, Alert, User){

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
}])

.controller('ResetConfirmController', ['$scope', '$routeParams', 'User', '$http', 'Alert', function($scope, $routeParams, User, $http, Alert){

	var token = $routeParams.token,
	uidb64 = $routeParams.uidb64;

	if(!!token && !!uidb64){
		$scope.sendNewPassword = function() {
			User.resetPasswordConfirm(uidb64, token, $scope.password1, function(res){
				if(res.status === "success"){
					Alert.add("Your password has been reset.","success");
				} else if (res.reason === "password_mismatch"){
						$scope.errorMessage = "Please try again, passwords don't match.";
				} else if (res.reason === "password_too_short"){
						$scope.errorMessage = "Please enter a password with at least 8 characters.";
				} else{
					Alert.add("This link has already been used.","danger");
				}
			});
		};
	} else {
		User.redirect("/reset");
	}

}])

.controller('HomeController',['$scope', '$sanitize', 'User','$analytics','$anchorScroll','$location',
	function($scope, $sanitize, User, $analytics, $anchorScroll,$location){

		$scope.betaSuccess = false;

		$scope.scrollTo = function(id) {
			$location.hash(id);
			$anchorScroll();
		};

		$scope.registerForBeta = function(){

			if($scope.betaForm.$valid){

				User.registerBeta($scope.email, function(data){
					// This callback is only called when return success
					$analytics.eventTrack('RegisterToBeta',
						{ category: 'Onboarding'});
					$scope.betaSuccess = true;
				});
			}
		};

		// Twitter share button
		!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');

	}])

.controller('OnboardingController', ['$scope', '$routeParams', 'Preference','Alert','$location','$anchorScroll','$window', '$rootScope', 'Basket', function($scope, $routeParams, Preference, Alert, $location, $anchorScroll, $window, $rootScope, Basket) {

	$scope.cuisines = [
	{ "name": "Italian", "image": "italy.png"},
	{ "name": "Chinese", "image": "china.png"},
	{ "name": "Indian", "image": "india.png"},
	{ "name": "Spanish", "image": "spain.png"},
	{ "name": "Thai",  "image": "thai.png"},
	{ "name": "French",  "image": "france.png"}
	];

	$scope.preference = Preference.getAll();
	$scope.number = 8;
	$scope.peopleIndex = 1;
	$scope.preference.days = 7;
	$scope.cookingValue = 50;

	$window.scrollTo(0,0);

	Basket.clearLocal();

	// Generate empty array for ng-repeat to display the people icons
	$scope.getNumber = function(num) {
		return new Array(num);
	};

	$scope.addDays = function(){
		if($scope.preference.days < 10) {
			$scope.preference.days++;
		}
	};

	$scope.removeDays = function(){
		if($scope.preference.days !==1) {
			$scope.preference.days--;
		}
	};

	$scope.generateBasket = function() {
		$scope.preference.people = $scope.peopleIndex+1;
		$scope.preference.price_sensitivity = parseInt($scope.cookingValue, 10) / 100;

		if(Preference.isNotValid($scope.preference)) {
			Alert.add("It looks like you didn't select all of your preferences.","danger");
			// Scroll to top
			$location.hash('wrap');
			$anchorScroll();
		}
		else {
			Preference.setParameters($scope.preference);
			$location.path("/basket");
		}
	};


	$rootScope.$on('peoplePosition', function(event, selectedIndex){
		$scope.peopleIndex = selectedIndex;
		$scope.$digest();
	});

	// JQuery logic in the controller because I don't have access to the
	// ui-slider directive - ugly but does the work
	angular.element('.slider-bar').bind('mouseup', function(){
		$scope.preference.price_sensitivity = $scope.cookingValue;
	});

}])

.controller('ProductListController',
	['$rootScope','$scope','Preference','Basket', 'Product', 'User','Tesco','Alert','$location','$anchorScroll', '$window', '$analytics','$modal', '$timeout',
	function($rootScope, $scope, Preference, Basket, Product, User, Tesco, Alert,$location,$anchorScroll,$window,$analytics,$modal,$timeout) {

		// Initialize variables for the frontend
		var preferenceList = Preference.getAll();

		$scope.tesco_response = {};
		$scope.user = {};
		$scope.tescoCredential = {};
		$scope.search_result = {};
		$scope.autocompleteResult = [];
		$scope.basketMessage = User.isLoggedIn();

		$scope.oldBasket = Basket.getLocal();
		var hasOldBasket = $scope.oldBasket.length !== 0;

		if(hasOldBasket){
			$scope.products = $scope.oldBasket;
			$scope.basketMessage = false
			$window.scrollTo(0,0);
		}

		$scope.getBasket = function() {

			// First action on the page -> load the recommended basket
			if(!Preference.isNotValid(preferenceList) || User.isLoggedIn()){
				$scope.loading = true;
				$scope.basketMessage = false;
				Basket.post(preferenceList, function(res){
					$scope.loading = false;
					$window.scrollTo(0,0);

					if(res.success === false){
						Alert.add("We couldn't create your basket.","danger");
					} else {
						// Flush temp basket
						Basket.addLocal([]);
						Basket.addOldRecommendation(res.recommended_basket);
						if(!User.isLoggedIn()) {
							Basket.setUserSettingsKey(res.user_settings_hash);
						} else {
							Basket.setRecommendedBasketId(res.recommended_basket_id);
						}

						$scope.products = Product.formatUI(res.recommended_basket);
						Basket.addLocal($scope.products);
					}

				});
			} else {
				Alert.add("Tell us what you like and we'll take care of your basket.","info");
				User.redirect("/start");
			}
		};

		if(!User.isLoggedIn() && !hasOldBasket) {
			$scope.getBasket();
		}

		$scope.clearResult = function(){
			$scope.search_result = {};
		};

		// GET search
		$scope.searchProducts = function(query){

			if(query) {
				Product.search(query,
					function(res){ // success
						$scope.search_result = Product.getQuantity(res, $scope.products);
						$window.onclick = function (event) {
							closeSearchWhenClickingElsewhere(event);
						};
					},function(res){ // error
						Alert.add("Could not find this product","danger");
						$scope.search_result = {};
					});
			} else {
				$scope.search_result = {};
			}
		};


		$scope.autoComplete = function(query) {
			if(typeof query === "undefined" || query.length === 0){ return [];}

			Product.autocomplete(query, function(res){
				$scope.autocompleteResult = [];

				angular.forEach(res.data, function(item){
					$scope.autocompleteResult.push(item.name);
				});
			});
		};

		// Forces user to loggin if he wants to transfer his basket
		$scope.transferBasket = function(){
			// When you open a form it will close the search
			$scope.clearResult();
			if(!$scope.products){
				Alert.add("You need to add products to your basket to checkout.", "info")
			} else {
				var modalInstance = $modal.open({
				templateUrl: 'static/app/partials/_modal.html',
				controller: 'ModalCtrl',
				resolve: {
					products: function () {
						return $scope.products;
					}
				}
				});
			}

		};

		$scope.addProduct = function(new_product) {
			if(new_product.quantity < 50){
				Product.add($scope.products, new_product);
				Basket.addLocal($scope.products);
			}
		};

		$scope.removeProduct = function(product) {
			Product.remove($scope.products, product);
			Basket.addLocal($scope.products);
		};

		$scope.getTotal = function(val1,val2) {
			return (parseFloat(val1.replace("GBP","")) * parseFloat(val2)).toFixed(2);
		};

		$scope.basketTotal = function() {
			return Product.getTotal($scope.products);
		};

		// When you remove a product from the directive you need to update the scope
		$rootScope.$on('deleteProduct', function(event, item){
			$scope.products = Product.delete($scope.products, item);
			$scope.$apply();
			Basket.addLocal($scope.products);
		});

		$rootScope.$on('searchEnter', function(event, query){
			$scope.searchProducts(query);
		});

		var closeSearchWhenClickingElsewhere = function(event){

			var clickedElement = event.target,
			parents = angular.element(clickedElement).parents(),
			clickedOnTheSearchPanel = false;

			// checks if the parents of the div is one of the following string
			for (var i = parents.length - 1; i >= 0; i--) {
				if(parents[i].className.indexOf("product-search-result") != -1 ||
					parents[i].className.indexOf("search-bar") != -1){
					clickedOnTheSearchPanel = true;
			}
		}

		if(!clickedOnTheSearchPanel){
			$scope.clearResult();
			$scope.$digest();
		}
	};

}])

.controller('ModalCtrl',
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
			list = products.map(function (v) {
				return v.products;
			}).reduce(function (a, b){
				return a.concat(b);
			});

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

	}])

.controller('RegistrationController', ['$scope','User','Alert', function($scope,User,Alert) {

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
}])

.controller('LoginController', ['$sanitize','$scope','User','Alert', function($sanitize,$scope,User,Alert) {
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

}])

.controller('ProfileController', ['$scope','User','Alert', function($scope, User,Alert){

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
}])

.controller('AlertController', ['$scope', 'Alert', '$timeout', '$location', function($scope, Alert, $timeout, $location) {


	$scope.alerts = Alert.getAll();

	$scope.closeAlert = function(index) {
		Alert.close(index);
		$scope.alerts = Alert.getAll();
	};

}]);

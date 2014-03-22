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
	uidb64 = $routeParams.uidb64,
	newPassword = 'test';

	if(!!token && !!uidb64){
		$scope.sendNewPassword = function() {
			User.resetPasswordConfirm(uidb64, token, newPassword, function(res){
				if(res.status === "success"){
					Alert.add("Your password has been reset.","success");
				}else{
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

.controller('OnboardingController', ['$scope', '$routeParams', 'Preference','Alert','$location','$anchorScroll','$window', '$rootScope', function($scope, $routeParams, Preference, Alert, $location, $anchorScroll, $window, $rootScope) {

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
	$scope.cookingValue = 20;

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
						Basket.addOldRecommendation(res.recommended_basket);
						if(!User.isLoggedIn()) {
							Basket.setUserSettingsKey(res.user_settings_hash);
						} else {
							Basket.setRecommendedBasketId(res.recommended_basket_id);
						}

						$scope.products = Product.formatUI(res.recommended_basket);
					}

				});
			} else {
				Alert.add("Tell us what you like and we'll take care of your basket.","info");
				User.redirect("/start");
			}
		};

		if(!User.isLoggedIn()) {
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

			var modalInstance = $modal.open({
				templateUrl: 'static/app/partials/_modal.html',
				controller: 'ModalCtrl',
				resolve: {
					products: function () {
						return $scope.products;
					}
				}
			});
		};

		$scope.addProduct = function(new_product) {
			Product.add($scope.products, new_product);
		};

		$scope.removeProduct = function(product) {
			Product.remove($scope.products, product);
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
	['$scope', '$modalInstance', 'products','User','$sanitize','Alert','Basket','Preference','Tesco', '$analytics',
	function($scope, $modalInstance, products, User, $sanitize,Alert,Basket,Preference,Tesco,$analytics){

		$scope.tescoCredential = {};
		$scope.user = {};
		$scope.unsuccessfulItems = [];

		$scope.signup = true; // shows sign up at first
		$scope.sendTescoForm = true;
		$scope.loggedin = false;
		$scope.notInvited = false;


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

			if(typeof user_settings_hash === "undefined") user_settings_hash = "";

			User.signup(user.email, user.password, user_settings_hash, function(res){
				if(res.success === false){
					$scope.toggleError = true;

					if(res.reason === "already_exist"){
						$scope.errorMessage = "This email has already been used.";
					} else {
						$scope.errorMessage = "You haven't been invited to the beta";
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
				// Alert.add("Successfully logged in.", "success");
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

					var unsuccessfulItems = Tesco.getUnsuccessful(res);

					if(unsuccessfulItems.length === 0){
						$analytics.eventTrack('SuccessfullyTransfered',
							{  category: 'BasketPorting'});
						$scope.unsuccessfulTransfer = false;
					} else{
						$analytics.eventTrack('UnsuccessfullyTransfered',
							{  category: 'BasketPorting'});
						$scope.unsuccessfulTransfer = true;
						$scope.unsuccessfulItems = unsuccessfulItems;
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
	$scope.updateEmail = function() {
		if($scope.settingsForm.$valid) {
			User.updateEmail($scope.email, function(res){
				Alert.add("Your email has been updated.","success");
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

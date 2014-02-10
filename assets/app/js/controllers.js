'use strict';

/* Controllers */

angular.module('App.controllers', ['ngSanitize','ui.bootstrap'])

.controller('HomeController',['$scope', '$sanitize', 'User','$analytics','$anchorScroll','$location',
	function($scope, $sanitize, User, $analytics, $anchorScroll,$location){

		$scope.email = [];
		$scope.betaSuccess = false;

		$scope.scrollTo = function(id) {
			$location.hash(id);
			$anchorScroll();
		}

		$scope.registerForBeta = function(){

			var email = $scope.email;

			if($scope.betaForm.$valid){

				User.registerBeta(email, function(data){
					// This callback is only called when return success
					$analytics.eventTrack('RegisterToBeta',
						{ category: 'Onboarding'});
					$scope.betaSuccess = true;
				});
			}
		};

	}])

.controller('OnboardingController', ['$scope', '$routeParams', 'Preference','Alert','$location','$anchorScroll','$window', function($scope, $routeParams, Preference, Alert, $location, $anchorScroll, $window) {

	$scope.cuisines = [{ "name": "Italian", "image": "italy.png"},
	{ "name": "Chinese", "image": "china.png"},
	{ "name": "Indian", "image": "india.png"},
	{ "name": "Spanish", "image": "spain.png"},
	{ "name": "Thai",  "image": "thai.png"},
	{ "name": "French",  "image": "france.png"}];

	$scope.preference = {};
	$scope.cookingValue = 10;
	$scope.cookingStyle = "minimal";


	// Persist data from local storage
	$scope.preference = Preference.getAll();

	var goToTop = function(){
		// set the location.hash to the id of
		// the element you wish to scroll to.
		$location.hash('wrap');
		$anchorScroll();
	};

	$scope.saveData = function() {

		Preference.setParameters($scope.preference);
		if(Preference.isNotValid(Preference.getAll())) {
			Alert.add("You didn't put the right informations.","danger");
			goToTop();
		} else {
			$location.path("/basket");
		}
		// if (page_id === 1) { //cuisine

		// 	if(Preference.getCuisine().length === 0) {
		// 		Alert.add("You didn't select a cuisine style.","danger");
		// 		goToTop();
		// 	} else {
		// 		$location.path("/onboarding/2");
		// 	}

		// } else if (page_id === 2) { //numbers page



		// } else { // Edge case
		// 	$location.path("/onboarding/1");
		// }
	};

	}])

.controller('ProductListController',
	['$rootScope','$scope','Preference','Basket', 'Product', 'User','Tesco','Alert','$location','$anchorScroll', '$window', '$analytics','$modal',
	function($rootScope, $scope, Preference, Basket, Product, User, Tesco, Alert,$location,$anchorScroll,$window,$analytics,$modal) {

		// Initialize variables for the frontend
		var preferenceList = Preference.getAll();
		$scope.tesco_response = {};
		$scope.user = {};
		$scope.tescoCredential = {};
		$scope.search_result = {};

		// When you remove a product from the directive you need to update the scope
		$rootScope.$on('removeProduct', function(event, $productIndex){
			$scope.products.splice($productIndex,1);
			$scope.$apply();
		});

		$rootScope.$on('searchEnter', function(event, query){
			$scope.searchProducts(query);
		});

		$scope.closeForm = function() {
			$scope.toggleForm(false);
		};

		$scope.closeTescoForm = function() {
			$scope.toggleTescoForm(false);
		};

		$scope.clearResult = function(){
			$scope.search_result = {};
		};

		// First action on the page -> load the recommended basket
		if(!Preference.isNotValid(preferenceList)){
			$scope.loading = true;

			Basket.post(preferenceList,
				function(res){
					$scope.loading = false;

					if(res.success === false){
						Alert.add("We couldn't create your basket.","danger");
					} else {
						Basket.addOldRecommendation(res);
						$scope.products = res;
					}
				});
		} else {
			Alert.add("Tell us what you like and we'll take care of your basket.","info");
			User.redirect("/onboarding/1");
		}

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

		$scope.results = [];

		$scope.autoComplete = function(query) {

			if(query === undefined){
				return [];
			}

			Product.autocomplete(query, function(res){

				var products = [];

				angular.forEach(res.data, function(item){
					products.push(item.name);
				});

				$scope.results = products;
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
			var $products = $scope.products,
			isPresent = false;

			for (var i = $products.length-1; i >= 0; i--) {
				if ($products[i].name === new_product.name) { //if it's in the list bump up the quantity
					isPresent = true;
				if($products[i].quantity>=100){
					$products[i].quantity = 100;
				} else{
					$products[i].quantity += 1;
				}
				break;
			}
		}

		if(!isPresent){
			new_product.quantity = 1;
			$scope.products.push(new_product);
		} else {
			$scope.products = $products;
		}
	};

	$scope.removeProduct = function(product) {
		var $products = $scope.products;

		for (var i = $products.length-1; i >= 0; i--) {
			if ($products[i].name === product.name) {
				$products[i].quantity -= 1;

				if($products[i].quantity === 0) {
					$products.splice(i,1);
				}

				break;
			}
		}

		$scope.products = $products;
	};

	$scope.getTotal = function(val1,val2) {
		return (parseFloat(val1.replace("GBP","")) * parseFloat(val2)).toFixed(2);
	};

	$scope.basketTotal = function() {
		var total = 0;
		angular.forEach($scope.products, function(value, key){
			total += parseFloat(value.price.replace("GBP","")) * parseInt(value.quantity,10);
		});

		return total.toFixed(2);
	};

	var closeSearchWhenClickingElsewhere = function(event){

		var clickedElement = event.target,
		parents = angular.element(clickedElement).parents(),
		clickedOnTheSearchPanel = false;

		// checks if the parents of the div is one of the following string
		for (var i = parents.length - 1; i >= 0; i--) {
			if(parents[i].className.indexOf("product-search-result") != -1
				|| parents[i].className.indexOf("search-bar") != -1){
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
			var user = $scope.user;
			User.signup(user.email, user.password, function(data){
			}, function(res,status){
				if(status == 401){
					$scope.notInvited = true;
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
			var tescoCredential = $scope.tescoCredential;
			var list = $scope.products;

			$scope.loading = true;
			$scope.sendTescoForm = false;

			var oldRecommendation = Basket.getOldRecommendation();
			var preference = Preference.getAll();

			$analytics.eventTrack('ClickToSend',
				{  category: 'BasketPorting'});

			if(products.length === 0 || products === undefined){ return; }

			Tesco.post(tescoCredential.email, tescoCredential.password, products, oldRecommendation, preference, function(res) {
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

			User.login(user.email, user.password, function(data){
				User.setLoggedIn(true);
				Alert.add("Successfully logged in.", "success");
				User.redirect("/");
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

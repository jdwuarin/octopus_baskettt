'use strict';

/* Controllers */

angular.module('App.controllers', ['ngSanitize','ui.bootstrap'])

	.controller('OnboardingController', ['$scope', '$routeParams', 'Preference','Alert','$location','$anchorScroll', function($scope, $routeParams, Preference, Alert, $location, $anchorScroll) {

		$scope.cuisines = [{ "name": "Italian", "image": "italian.png"},
		{ "name": "Chinese", "image": "chinese.png"},
		{ "name": "Indian", "image": "indian.png"},
		{ "name": "Spanish", "image": "spanish.png"},
		{ "name": "Thai",  "image": "thai.png"},
		{ "name": "French",  "image": "french.png"}];

		$scope.preference = {};

		var page_id = parseInt($routeParams.id,10);

		$scope.page = page_id;

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

			if (page_id === 1) { //cuisine

				if(Preference.getCuisine().length === 0) {
					Alert.add("You didn't select a cuisine style.","danger");
					goToTop();
				} else {
					$location.path("/onboarding/2");
				}

			} else if (page_id === 2) { //numbers page

				if(Preference.isNotValid(Preference.getAll())) {
					Alert.add("You didn't put the right informations.","danger");
					goToTop();
				} else {
					$location.path("/basket");
				}

			} else { // Edge case
				$location.path("/onboarding/1");
			}
		};

		$scope.isActive = function(id) {
			return id === page_id;
		};

	}])

	.controller('ProductListController', ['$rootScope','$scope','Preference','Basket', 'Product', 'User','Tesco','Alert','$location','$anchorScroll', '$window',function($rootScope, $scope, Preference, Basket, Product, User, Tesco, Alert,$location,$anchorScroll,$window) {

		// Initialize variables for the frontend
		var preferenceList = Preference.getAll();

		$scope.user = {};
		$scope.tescoCredential = {};
		$scope.search_result = {};

		// When you close the signup form the Tesco form comes
		$rootScope.$on('CloseSignUpForm', function(){
			$scope.closeForm();
			$scope.toggleTescoForm(true);
		});

		// When you remove a product from the directive you need to update the scope
		$rootScope.$on('removeProduct', function(event, $productIndex){
			$scope.products.splice($productIndex,1);
			$scope.$apply();
		});

		$scope.showBasketDetails = function() {
			$rootScope.$emit('showBasketDetails');
		};

		$scope.closeForm = function() {
			$scope.toggleForm(false);
		};

		$scope.closeTescoForm = function() {
			$scope.toggleTescoForm(false);
		};

		$scope.clearSearch = function(){
			$scope.search_result = {};
			$scope.queryTerm ="";
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
		$scope.searchProducts = function(){
			if($scope.queryTerm) {
				Product.search($scope.queryTerm,
					function(res){ // success
						$scope.search_result = res;
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

		// Forces user to loggin if he wants to transfer his basket
		$scope.transferBasket = function(){
			// When you open a form it will close the search
			$scope.clearSearch();

			if(!User.isLoggedIn()) {
				$scope.toggleForm(true);
			} else {
				$scope.toggleTescoForm(true);
			}
		};

		$scope.signup = function(){
			var user = $scope.user;
			if($scope.signupForm.$valid){

				User.signup(user.email, user.password, function(data){
					$rootScope.$emit('UserSignedUp');
				});
			}
		};

		$scope.sendToTesco = function(){
			var tescoCredential = $scope.tescoCredential;
			var list = $scope.products;

			if ($scope.tescoForm.$valid) {
				$scope.toggleTescoForm(false);
				$scope.loading = true;
				var oldRecommendation = Basket.getOldRecommendation();

				Tesco.post(tescoCredential.email, tescoCredential.password, list, oldRecommendation, function(res) {
					$scope.loading = false;
					if(Tesco.getUnsuccesful(res).length === 0){
						Alert.add("Your products have been transfered to Tesco","success");
					} else{
						Alert.add("Some products couldn't be transfered","danger");
					}

				});
			}
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
		};

		if(!clickedOnTheSearchPanel){
			$scope.clearSearch();
			$scope.$digest();
		}
	};

	}])

	.controller('RegistrationController', ['$scope','User', function($scope,User) {

		$scope.user = {};

		$scope.signup = function(){
			var user = $scope.user;
			if($scope.signupForm.$valid){

				User.signup(user.email, user.password, function(data){
					// This callback is only called when return success
					User.redirect("/");
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

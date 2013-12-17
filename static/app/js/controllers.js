'use strict';

/* Controllers */

angular.module('App.controllers', ['ngSanitize','ui.bootstrap'])

	.controller('OnboardingController', ['$scope', '$routeParams', 'Preference', function($scope, $routeParams, Preference) {

		$scope.cuisines = [{ "name": "Italian", "image": "italian.png"},
		{ "name": "Chinese", "image": "chinese.png"},
		{ "name": "Indian", "image": "indian.png"},
		{ "name": "Spanish", "image": "spanish.png"},
		{ "name": "Thai",  "image": "thai.png"},
		{ "name": "French",  "image": "french.png"}];

		$scope.preference = {};

		var page_id = parseInt($routeParams.id,10);

		$scope.page = page_id;


		$scope.saveData = function() {
			if(page_id === 2) {
				Preference.setPeople($scope.preference.people);
			} else if (page_id === 3) {
				Preference.setBudget($scope.preference.budget);
			}
		};

		$scope.isActive = function(id) {
			return id === page_id;
		};

		$scope.getNextPage = function() {
			// The onboarding process only has 3 steps
			if(page_id < 3 && page_id > 0) {
				return "#/onboarding/" + (page_id+1).toString();
			// When you're done with the onboarding you're transfered to the product list
			} else if(page_id === 3) {
				return "#/basket";
			// Edge case
			} else {
				return "#/";
			}
		};


	}])

	.controller('ProductListController', ['$rootScope','$scope','Preference','Basket', 'Product', 'User','Tesco','Alert',function($rootScope, $scope, Preference, Basket, Product, User, Tesco, Alert) {

		var preferenceList = Preference.getAll();
		$scope.user = {};
		$scope.tescoCredential = {};


		$rootScope.$on('CloseSignUpForm', function(){
			$scope.closeForm();
			$scope.toggleTescoForm(true);
		});
		
		Basket.post(preferenceList, function(res){
			$scope.products = res;
		});

		$scope.resetSelection = function(){
			$scope.$broadcast('resetSelection');
		};

		$scope.searchProducts = function(){
			Product.search($scope.queryTerm, function(res){
				$scope.search_result = res;
			});
		};

		$scope.transferBasket = function(){
			if(!User.isLoggedIn()) {
				$scope.toggleForm(true);
			} else {
				$scope.toggleTescoForm(true);
			}
		};

		$scope.closeForm = function() {
			$scope.toggleForm(false);
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
			var list = [1,2,3];

			if ($scope.tescoForm.$valid) {
				$scope.toggleTescoForm(false);
				$scope.viewLoading = true;
				Tesco.post(tescoCredential.email, tescoCredential.password, list, function(res) {
					$scope.viewLoading = false;
					Alert.add("Your products have been transfered to Tesco","success");
				});
			}
		};

		$scope.closeTescoForm = function() {
			$scope.toggleTescoForm(false);
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
					Alert.add("Successfully logged in.", "success")
					User.redirect("/");
				});
			}
		};

	}])

	.controller('AlertController', ['$scope', 'Alert', function($scope, Alert) {

		$scope.alerts = Alert.getAll();

		$scope.closeAlert = function(index) {
			Alert.close(index);
			$scope.alerts = Alert.getAll();
		};

	}]);

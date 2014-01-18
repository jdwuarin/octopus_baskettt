'use strict';

/* Services */

angular.module('App.services', ['LocalStorageModule'])

	// Factory that uses the REST api/v1
	.factory('Product', ['$http', function($http) {

		function getUrl(id) {
			id = typeof id !== 'undefined' ? id : ''; //if no id put empty string i.e. for get all products
			return 'api/v1/product/' + id + '?format=json';
		}

		return {
			get: function(id, callback) { // GET /id
				return $http.get(getUrl(id)).success(callback);
			},
			query: function(callback) { // GET /
				return $http.get(getUrl()).success(callback);
			},
			save:function(product,callback) {
				return $http.post(getUrl(), product).success(callback);
			},
			remove: function(id, callback) {
				return $http.delete(getUrl(id)).success(callback);
			},
			put: function(product, callback) {
				return $http.put(getUrl(product.id), product).success(callback);
			},
			search: function(term, callback, errorcb) {
				return $http.get(getUrl("search/") + "&term=" + term).success(callback).error(errorcb);
			}
		};
	}])

	// Factory that uses our user api
	.factory('User', ['$cookies', '$http', '$location', function($cookies, $http, $location) {

		function getUrl(req) {
			return 'api/v1/user/' + req + '/?format=json';
		}

		var LoggedIn = null;

		return {
			login: function(email, password, callback) { // POST /user/login
				return $http({
					url: getUrl('login'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback);
			},
			logout: function(callback) { // GET /user/logout
				return $http({
					url: getUrl('logout'),
					method: "GET"
				}).success(callback);
			},
			redirect: function(url){
				// Redirect to the given url (defaults to '/')
				url = url || '/';
				$location.path(url);
			},
			isLoggedIn: function() {
				return LoggedIn;
			},
			setLoggedIn: function(val) {
				LoggedIn = val;
			},
			signup: function(email, password, callback) {
				return $http({
					url: getUrl('signup'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback);
			},
			// Check if logged in in Django backend
			// Avoid losing a session when a user reloads the page
			requestLoggedIn: function(callback) {
				return $http({
					url: 'api/v1/user/current/?format=json',
					method: "GET",
					headers: {'Content-Type': 'application/json'},
				}).success(callback);
			}
		};
	}])

	// Service that contains the preferences in the onboarding
	.service('Preference', ['localStorage','Alert', function(localStorage, Alert) {

		var preferenceList = {};
		preferenceList.cuisine= [];

		var isUndefined = function(variable){
			return typeof variable == "undefined";
		};

		return {
			getCuisine: function() {

				var local_cuisine = localStorage.get('preferences').cuisine;

				// If we haven't saved any preferences in local storage take the temporary one
				if(local_cuisine) {
					return local_cuisine;
				} else {
					return preferenceList.cuisine;
				}
			},
			setCuisine: function(scope) {

				var isPresent = false;

				for (var i = preferenceList.cuisine.length-1; i >= 0; i--) {
						//if it's already in the list
						if (preferenceList.cuisine[i] == scope.cuisine.name) {
							isPresent = true;

							if(!scope.selectedStatus){
								preferenceList.cuisine.splice(i,1);
							}
						}
				}

				if (!isPresent && scope.selectedStatus) {
					preferenceList.cuisine.push(scope.cuisine.name);
					var cuisine_str = JSON.stringify(preferenceList);
					localStorage.add('preferences', cuisine_str);
				}
			},
			setParameters: function(preferences) {

				preferenceList.cuisine = this.getCuisine();
				preferenceList.people = preferences.people;
				preferenceList.days   = preferences.days;
				preferenceList.budget = preferences.budget;

				var pref_str = JSON.stringify(preferenceList);
				localStorage.add('preferences', pref_str);

			},
			getAll: function() {
				// On some browser it crashes when preferences has no cuisine
				// We'll init the localstorage first
				if(!localStorage.get('preferences')) {
					var init = JSON.stringify(preferenceList);
					localStorage.add('preferences',init);
				}

				return localStorage.get('preferences');
			},
			isNotValid: function(list) {

				// First check to avoid an error with length
				if(isUndefined(list.cuisine) ||
					isUndefined(list.people) ||
					isUndefined(list.budget) ||
					isUndefined(list.days)) {
					return true;
				}

				if(list.cuisine.length === 0 ||
					list.people.length === 0 ||
					list.budget.length === 0 ||
					list.days.length === 0) {
					return true;
				} else {
					return false;
				}
			}
		};
	}])


	// Factory that uses that keeps the data during the onboarding
	.factory('localStorage', ['localStorageService', function(localStorageService) {

		return {
			add: function(key, value) {
				localStorageService.add(key, value);
			},

			get: function(key) {
				return localStorageService.get(key);
			}
		};

	}])

	.factory('Basket',  ['$http','localStorage', function($http,localStorage) {
		var productList = {};

		return {
			// Get recommendation from our backend
			post: function(preferences, callback, errorcb) {
				return $http({
					url: 'api/v1/user/basket/?format=json',
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: preferences
				}).success(callback);
			},
			add: function(product) {
				productList.push(product);
			},
			getAll: function() {
				return productList;
			},
			addOldRecommendation: function(list){
				localStorage.add('oldRecommendation',list);
			},
			getOldRecommendation: function(list){
				return localStorage.get('oldRecommendation');
			}
		};

	}])

	.factory('Tesco',  ['$http', function($http) {

		return {
			// Populate tesco basket
			post: function(email, password, list, recommendation, callback) {
				return $http({
					url: 'port_basket/?format=json',
					method: 'POST',
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password, products:list, recommendation: recommendation}
				}).success(callback);
			},
			getUnsuccesful: function(basket){
				var false_list = [];

				angular.forEach(basket, function(value, key){
					if(value == "False") {
						false_list.push(value);
					}
				});
				return false_list;
			}
		};

	}])

	.factory('Alert',  ['$timeout',function($timeout) {

		var alertList = [];

		return {
			add: function(message, type) {
				var alreadyExist = false;

				alreadyExist = angular.forEach(alertList, function(value, key){
					if(value === message){
						return true;
					}
				});

				if(alreadyExist && (alertList.length !== 0)){
					return;
				}

				var $this = this,
				randomId = Math.random();

				$timeout(function(){
					$this.close(randomId);
				}, 5000);

				alertList.push({msg: message, type: type, id: randomId});
			},
			close: function(id) {
				angular.forEach(alertList, function(value, index){
					if(value.id === id){
						alertList.splice(index, 1);
					}
				});
			},
			getAll: function() {
				return alertList;
			},
			flush: function(){
				alertList = [];
			}
		};

	}]);

'use strict';

/* Services */


angular.module('App.services', ['LocalStorageModule'])

	// Factory that uses the REST api/v1
	.factory('Product', ['$http', function($http) {

		function getUrl(id) {
			id = typeof id !== 'undefined' ? id : ''; //if no id put empty string i.e. for get all products
			return 'http://127.0.0.1:8000/api/v1/product/' + id + '?format=json';
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
			}
		};
	}])

	// Factory that uses the apiray API for the recipes
	.factory('Recipe', ['$http', function($http) {

		function getUrl() {
			return 'http://baskettt.apiary.io/recipes';
		}

		return {
			query: function(callback) { // GET /
				return $http.get(getUrl()).success(callback);
			}
		};
	}])

	// Factory that uses our user api
	.factory('User', ['$cookies', '$http', '$location', function($cookies, $http, $location) {

		function getUrl(req) {
			return 'http://127.0.0.1:8000/api/v1/user/' + req + '/?format=json';
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
					url: 'http://127.0.0.1:8000/api/v1/user/current/?format=json',
					method: "GET",
					headers: {'Content-Type': 'application/json'},
				}).success(callback);
			}
		};
	}])

	// Service that contains the preferences in the onboarding
	.service('Preference', [function() {

		var preferenceList = {};
		preferenceList.cuisine= [];

		return {
			getCuisine: function() {
				return preferenceList.cuisine;
			},
			setCuisine: function(scope) {

				var isPresent = false;
				
				for (var i = preferenceList.cuisine.length-1; i >= 0; i--) {

						if (preferenceList.cuisine[i] == scope.cuisine.name) { //if it's in the list
							isPresent = true;

							if(!scope.selectedStatus){
								preferenceList.cuisine.splice(i,1);
							}
						}
				}

				if (!isPresent && scope.selectedStatus) {
					preferenceList.cuisine.push(scope.cuisine.name);
				}
			},
			setPeople: function(count) {
				preferenceList.people = count;
			},
			setBudget: function(amount) {
				preferenceList.budget = amount;
			},
			getAll: function() {
				return preferenceList;
			}
		};
	}])

	// Factory that uses the recommendation backend
	.factory('Recommendation', ['$http', function($http) {

		function getUrl() {
			return 'http://127.0.0.1:8000/recommendation/';
		}

		return {
			post: function(ids, callback) { // POST /recommendation

				return $http({
					url: getUrl(),
					method: "POST",
					headers: {'Content-Type': 'application/x-www-form-urlencoded'},
					data: "sa mere"
				}).success(callback);
			}
		};
	}])

	// Factory that uses that keeps the data during the onboarding
	.factory('localStorage',  ['localStorageService', function(localStorageService) {

		return {
			add: function(key, value) {
				localStorageService.add(key, value);
			},

			get: function(key) {
				return localStorageService.get(key);
			}
		};

	}])

	.factory('Basket',  ['$http', function($http) {

		return {
			post: function(list, callback) {
				return $http.get('static/app/js/product.json').success(callback);
				// return $http({
				// 	url: 'http://127.0.0.1:8000/api/v1/user/basket/?format=json',
				// 	method: "POST",
				// 	headers: {'Content-Type': 'application/json'},
				// 	data: list
				// })
			}
		};

	}]);

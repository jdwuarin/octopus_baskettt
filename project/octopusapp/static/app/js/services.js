'use strict';

/* Services */


angular.module('App.services', [])

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
	.factory('User', ['$http', function($http) {

		function getUrl(id) {
			id = typeof id !== 'undefined' ? id : ''; //if no id put empty string i.e. for get all products
			return 'http://127.0.0.1:8000/api/v1/user/login/?format=json';
		}

		return {
			login: function(email, password, callback) { // POST /user/login
				return $http({
					url: getUrl(),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback);
			}
		};
	}])

	// Service that contains the ids of the selected recipes
	.service('selectedRecipes', [function() {

		var productList = [];

		return {
			getObjects: function() {
				return productList;
			},
			setObjects: function(value) {
				var isPresent = false;
				productList.forEach(function(element, index, array) {
					if(element === value) {
						productList.splice(index,1);
						isPresent = true;
					}
				});

				if (!isPresent){
					productList.push(value);
				}
			}
		}
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
	}]);
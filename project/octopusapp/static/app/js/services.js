'use strict';

/* Services */


angular.module('App.services', []).
	// Factory that uses the REST api/v1
	factory('Product', ['$http', function($http) {

		function getUrl(id) {
			id = typeof id !== 'undefined' ? id : ''; //if no id put empty string i.e. for get all products
			return 'http://127.0.0.1:8000/api/v1/product/' + id + '?format=json&callback=';
		}

		return {
			get: function(id, callback) {
				return $http.get(getUrl(id)).success(callback);
			},
			query: function(callback) {
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
	}]);

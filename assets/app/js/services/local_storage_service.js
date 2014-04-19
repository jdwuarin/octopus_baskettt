angular.module('App.services').factory('localStorage',
	['localStorageService',
	function(localStorageService) {

		return {
			add: function(key, value) {
				localStorageService.add(key, value);
			},

			get: function(key) {
				return localStorageService.get(key);
			},
			flush: function(){
				localStorageService.clearAll();
			}
		};

	}]);


angular.module('App.services').factory('Alert',
	['$timeout',
	function($timeout) {

		var alertList = [];

		return {
			add: function(message, type) {
				var alreadyExist = false;

				alreadyExist = angular.forEach(alertList, function(value, key){
					if(value === message){ return true; }
				});

				if(alreadyExist && (alertList.length !== 0)){ return; }

				var $this = this,
				randomId = Math.random();

				$timeout(function(){
					$this.close(randomId);
				}, 3000);

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


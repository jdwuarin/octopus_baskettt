angular.module('App.services').factory('Tesco',
	['$http',
	function($http) {

		return {
			// Populate tesco basket
			post: function(email, password, list, recommendation, preference, user_settings_hash, recommended_basket_id, callback) {

				return $http({
					url: 'port_basket/?format=json',
					method: 'POST',
					headers: {'Content-Type': 'application/json'},
					data: {
						email:email,
						password:password,
						products:list,
						recommended_basket: recommendation,
						settings: preference,
						user_settings_hash: user_settings_hash,
						recommended_basket_id: recommended_basket_id
					}
				}).success(callback);
			},
			getUnsuccessful: function(basket){
				var false_list = [];
				angular.forEach(basket.product_list, function(value, key){

					if(value.success == "False") {
						false_list.push(value);
					}
				});
				return false_list;
			}
		};

	}])



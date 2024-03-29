angular.module('App.services').factory('Basket',
	['$http','localStorage','Cart',
	function($http, localStorage, Cart){

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
			},
			getUserSettingsKey: function(){
				return localStorage.get('user_settings_hash');
			},
			setUserSettingsKey: function(user_settings_hash){
				localStorage.add('user_settings_hash',user_settings_hash);
			},
			getRecommendedBasketId: function() {
				var lsId = localStorage.get('recommended_basket_id');
				if(typeof lsId === "undefined"){
					lsId = "";
				}
				return lsId;
			},
			setRecommendedBasketId: function(id) {
				localStorage.add('recommended_basket_id', id);
			},
			addLocal: function(currentBasket){
				localStorage.add('current_basket', currentBasket);
			},
			getLocal: function(){
				var currentBasket = localStorage.get('current_basket');
				if(currentBasket === null){
					currentBasket = [];
				}
				return currentBasket;
			},
			clearLocal: function(){
				localStorage.add('current_basket', []);
			},
			create: function(params){
				return $http({
					url: 'api/v2/baskets/?format=json',
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: params
				});
			},
			fetchAll: function(){
				return $http({
					url: 'api/v2/baskets/?format=json',
					method: "GET",
					headers: {'Content-Type': 'application/json'},
				});
			},
			query: function(params){
				var self = this;
				return $http({
					url: 'api/v2/baskets/' + params.hash + '?format=json',
					method: "GET",
					headers: {'Content-Type': 'application/json'},
				}).then(function(res){

					var basket = res.data;
					basket.products = basket.product_dict.map(function(b){
						b.quantity = 1;
						return b;
					});
					var cart = [];
					cart.push(basket);
					Cart.setCart(cart);
					return cart;
				});
			}
		};

	}]);


angular.module('App.services').factory('Cart',
	['$http',
	function($http) {

		var self = this;
		self.cart = [];

		return {
			init: function(){
				self.cart.push({
					name: "BBQ with friends",
					products: [
						{
							name: "Tesco courgette",
							price: "2.00"
						}
					]
				});
				return self.cart;
			},
			add: function(newProduct, basketName) {
				console.log(newProduct, basketName);
				var isPresent = false;
				var index = -1;

				if(newProduct.quantity > 50) { return self.cart; }

				angular.forEach(self.cart, function(basket, i) {
					if(basket.name === basketName) { index = i; }
				});

				if(index === -1) { return self.cart; } // basket doesn't exist

				self.cart[index]["products"].map(function(product){
					if ((product.name === newProduct.name) &&
						(product.price === newProduct.price)) {
						isPresent = true;
						product.quantity += 1;
					}
					return product;
				});

				if(!isPresent) {
					newProduct.quantity = 1;
					self.cart[index]["products"].push(newProduct);
				}

				return self.cart;
			},

			updateBasketTotal: function(basketName) {

			},

			addBasket: function(basketName) {
				if(basketName.length === 0) { return self.cart; }

				var doesntExist = self.cart.filter(function(basket){
					return basket.name === basketName;
				}).length === 0 ;

				if(doesntExist) {
					self.cart.push({
						name: basketName,
						products: []
					});
				}

				return self.cart;

			}
		};

	}]);


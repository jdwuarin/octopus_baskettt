angular.module('App.services').factory('Cart',
	['$http',
	function($http) {

		var self = this;
		self.cart = [
		{
			name: "My basket",
			products: []
		}
		];

		return {
			init: function(){
				return self.cart;
			},

			add: function(newProduct) {
				var isPresent = false;
				var index = -1;
				// var basketName = newProduct.selectedbasketName;
				var basketName = "My basket";

				console.log("add that shit", newProduct);
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

				console.log(self.cart);
				return self.cart;
			},

			remove: function(productToRemove){
				var basketName = "My basket";
				var index = -1;

				if(productToRemove.quantity < 1) { return self.cart; }

				angular.forEach(self.cart, function(basket, i) {
					if(basket.name === basketName) { index = i; }
				});

				self.cart[index]["products"] = self.cart[index]["products"].map(function(product){
					if ((product.name === productToRemove.name) &&
						(product.price === productToRemove.price)) {
						product.quantity -= 1;
					}

					return product.quantity === 0 ? {} : product;
				}).filter(function(p){ return !!p.price; });

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
			},

			computeTotal: function() {
				var total = 0;

				self.cart.forEach(function(basket) {
					basket.products.forEach(function(product) {
						if(product.price && product.quantity){
							total += parseFloat(product.price.replace("GBP","")) * parseInt(product.quantity,10);
						}
					});
				});
				console.log(total, self.cart);

				return 'GBP'+total;
			},

			getProducts: function(){

				var allProducts=[];

				self.cart.forEach(function(basket){
					basket.products.forEach(function(product){
						allProducts.push(product);
					});
				});


				return allProducts;
			}
		};

	}]);


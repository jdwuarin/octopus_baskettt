angular.module('App.services').factory('Cart',
	['$http',
	function($http) {

		var self = this;
		self.cart = [
		{
			name: "My weekly groceries",
			products: [
			// {
			// 	department: "Food Cupboard",
			// 	id: 3884,
			// 	img: "http://img.tesco.com/Groceries/pi/886/5000157024886/IDShot_225x225.jpg",
			// 	link: "/groceries/Product/Details/?id=252004443",
			// 	name: "Heinz Baked Beans In Tomato Sauce 415G X 4 Pack",
			// 	price: "GBP2.50",
			// 	quantity: 1
			// },
			// {
		// 		department: "Food Cupboard",
		// 		id: 3884,
		// 		img: "http://img.tesco.com/Groceries/pi/886/5000157024886/IDShot_225x225.jpg",
		// 		link: "/groceries/Product/Details/?id=252004443",
		// 		name: "Heinz Baked Beans In Tomato Sauce 415G X 4 Pack",
		// 		price: "GBP2.50",
		// 		quantity: 1
		// 	}
			]
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
				var basketName = "My weekly groceries";

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
						total += parseFloat(product.price.replace("GBP","")) * parseInt(product.quantity,10);
					});
				});
				console.log(total, self.cart);

				return total;
			}
		};

	}]);


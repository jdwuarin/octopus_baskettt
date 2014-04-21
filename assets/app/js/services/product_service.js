angular.module('App.services').factory('Product',
	['$http', '$q', 'Alert',
	function($http, $q, Alert) {

		var self = this;

		function getUrl(id) {
			id = typeof id !== 'undefined' ? id : ''; //if no id put empty string i.e. for get all products
			return 'api/v1/product/' + id + '?format=json';
		}

		return {
			search: function(term) {

				if(term && term.length === 0){ return []; }

				return $http.get(getUrl("search/") + "&term=" + term)
				.then(function(res) {
					if(res.data.length === 0) {
						Alert.add("Could not find this product","danger");
						return $q.reject(res);
					}
					return res.data;
				}, function(res) {
					return $q.reject(res);
				});
			},
			autocomplete: function(term) {
				if(term && term.length === 0){ return []; }

				return $http.get(getUrl('autocomplete')+ "&term=" + term)
				.then(function(res) {
					return res.data.map(function(product) {
						return product.name;
					});
				}, function(res) {
					return $q.reject(res);
				});
			},
			getQuantity: function(searchItems, basketItems){
				// Oh lord that's ugly
				for (var i = 0; i < searchItems.length; i++) {

					searchItems[i]["quantity"] = 0;

					for (var j = 0; j < basketItems.length; j++) {
						if(searchItems[i].id === basketItems[j].id ){
							searchItems[i]["quantity"] = basketItems[j].quantity;
						}
					}
				}

				return searchItems;
			},
			formatUI: function(productSets) {

				var mainProducts = productSets.map(function (productSet) {
					if(productSet["main"]) {
						productSet["main"]["quantity"]=(productSet.quantity);
					}
					return productSet["main"];
				}).filter(function (product) {
					return !!product;
				});

				var byDepartment = {};
				mainProducts.forEach(function (product) {
					var department = product.department;
					if (!byDepartment[department]) {
						byDepartment[department] = [];
					}
					byDepartment[department].push(product);
				});

				var result = Object.keys(byDepartment).sort(function (a, b) {
					return byDepartment[b].length - byDepartment[a].length;
				}).map(function (name) {
					return {
						name: name,
						products: byDepartment[name]
					};
				});

				return result;
			},
			getTotal: function(productSets) {
				var total = 0;

				if(typeof productSets === "undefined") { return 0; }

				// Flatten the array
				var productList = productSets.map(function (v) {
					return v.products;
				}).reduce(function (a, b){
					return a.concat(b);
				});

				productList.forEach(function (p) {
					total += parseFloat(p.price.replace("GBP","")) * parseInt(p.quantity,10);
				});

				return total.toFixed(2);
			},
			delete: function($products, item) {

				for (var i = $products.length-1; i >= 0; i--) {
					$products[i]["products"] = $products[i]["products"].map(function (p) {
						if(p.name === item.name) { p.quantity = 0; }
						return p;
					}).filter(function (p) {
						return p.quantity > 0;
					});
				}

				return $products;
			},
			add: function(newProduct){



				// var isPresent = false,
				// index = -1;

				// $products.map(function (d, i) {
				// 	if(d.name === item.department) { index = i; }
				// });

				// // If new department
				// if (index === -1) {
				// 	$products.push({
				// 		name: item.department,
				// 		products: [item]
				// 	});
				// } else {

				// 	$products[index]["products"] = $products[index]["products"].map(function (p) {
				// 		if(p.name === item.name){
				// 			p.quantity += 1;
				// 			isPresent = true;
				// 		}
				// 		return p;
				// 	});

				// 	// If new product in existing department
				// 	if(!isPresent) {
				// 		item.quantity = 1;
				// 		$products[index]["products"].push(item);
				// 	}
				// }
				// return $products;
			},
			remove: function($products, item) {

				for (var i = $products.length-1; i >= 0; i--) {

					$products[i]["products"] = $products[i]["products"].map(function (p) {
						if(p.name === item.name) { p.quantity -= 1; }
						return p;
					}).filter(function (p) {
						return p.quantity > 0;
					});
				}

				return $products;
			}

		};
	}]);

'use strict';

/* Services */

angular.module('App.services', ['LocalStorageModule'])

	// Factory that uses the REST api/v1
	.factory('Product', ['$http', function($http) {

		function getUrl(id) {
			id = typeof id !== 'undefined' ? id : ''; //if no id put empty string i.e. for get all products
			return 'api/v1/product/' + id + '?format=json';
		}

		return {
			search: function(term, callback, errorcb) {
				return $http.get(getUrl("search/") + "&term=" + term).success(callback).error(errorcb);
			},
			autocomplete: function(term, callback) {
				return $http.get(getUrl('autocomplete')+ "&term=" + term).then(callback);
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
			add: function($products, item){

				var isPresent = false,
				index = -1;

				$products.map(function (d, i) {
					if(d.name === item.department) { index = i; }
				});

				// If new department
				if (index === -1) {
					$products.push({
						name: item.department,
						products: [item]
					});
				} else {

					$products[index]["products"] = $products[index]["products"].map(function (p) {
						if(p.name === item.name){
							p.quantity += 1;
							isPresent = true;
						}
						return p;
					});

					// If new product in existing department
					if(!isPresent) {
						item.quantity = 1;
						$products[index]["products"].push(item);
					}
				}
				return $products;
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
	}])

	// Factory that uses our user api
	.factory('User', ['$cookies', '$http', '$location', '$route', function($cookies, $http, $location, $route) {

		function getUrl(req) {
			return 'api/v1/user/' + req + '/?format=json';
		}

		var LoggedIn = (angular.copy(window.activeUser).length !== 0);

		return {
			login: function(email, password, callback,errorcb) { // POST /user/login
				return $http({
					url: getUrl('login'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback).error(errorcb);
			},
			logout: function(callback) { // GET /user/logout
				return $http({
					url: getUrl('logout'),
					method: "GET"
				}).success(callback);
			},
			redirect: function(url){
				// Redirect to the given url (defaults to '/')
				url = url || '/';
				$location.path(url);
			},
			isLoggedIn: function() {
				return LoggedIn;
			},
			setLoggedIn: function(val) {
				LoggedIn = val;
			},
			signup: function(email, password, callback, errorcb) {
				return $http({
					url: getUrl('signup'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password}
				}).success(callback).error(errorcb);
			},
			registerBeta: function(email, callback) {
				return $http({
					url: getUrl('beta_subscription'),
					method: "POST",
					headers: {'Content-Type': 'application/json'},
					data: {email:email}
				}).success(callback);
			}
		};
	}])

	// Service that contains the preferences in the onboarding
	.service('Preference', [ function() {

		var preferenceList = {};
		preferenceList.cuisine= [];

		var isUndefined = function(variable){
			return typeof variable == "undefined";
		};

		return {
			setCuisine: function(cuisineName, presentStatus) {

				var position = preferenceList.cuisine.indexOf(cuisineName);

				if(position === -1 && presentStatus){
					preferenceList.cuisine.push(cuisineName);
				} else if(!presentStatus){
					preferenceList.cuisine.splice(position,1);
				}

			},
			setParameters: function(preferences) {

				preferenceList.cuisine = preferences.cuisine;
				preferenceList.price_sensitivity  = preferences.price_sensitivity;
				preferenceList.people = preferences.people;
				preferenceList.days = preferences.days;

			},
			getAll: function() {
				return preferenceList;
			},
			isNotValid: function(list) {

				// First check to avoid an error with length
				if(isUndefined(list.cuisine) ||
					isUndefined(list.people) ||
					isUndefined(list.price_sensitivity) ||
					isUndefined(list.days)) {
					return true;
				} else if(list.cuisine.length === 0 ||
					list.people.length === 0 ||
					list.price_sensitivity.length === 0 ||
					list.days.length === 0) {
					return true;
				} else if(list.people < 0 ||
					list.price_sensitivity < 0 ||
					list.price_sensitivity > 1 ||
					list.days < 0){
					return true;
				}
				else {
					return false;
				}
			}
		};
	}])


	// Factory that uses that keeps the data during the onboarding
	.factory('localStorage', ['localStorageService', function(localStorageService) {

		return {
			add: function(key, value) {
				localStorageService.add(key, value);
			},

			get: function(key) {
				return localStorageService.get(key);
			}
		};

	}])

	.factory('Basket',  ['$http','localStorage', function($http,localStorage) {
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
			setUserSettingsKey: function(list){
				var key = list.map(function(p){
					return p["user_settings_hash"];
				}).filter(function(p){
					return !!p;
				});
				localStorage.add('user_settings_hash',key[0]);
			}
		};

	}])

	.factory('Tesco',  ['$http', function($http) {

		return {
			// Populate tesco basket
			post: function(email, password, list, recommendation, preference, user_settings_hash, callback) {

				return $http({
					url: 'port_basket/?format=json',
					method: 'POST',
					headers: {'Content-Type': 'application/json'},
					data: {email:email, password:password, products:list, recommendation: recommendation, settings: preference, user_settings_hash: user_settings_hash}
				}).success(callback);
			},
			getUnsuccessful: function(basket){
				var false_list = [];
				// console.log(basket);
				angular.forEach(basket, function(value, key){

					if(value.success == "False") {
						false_list.push(value);
					}
				});
				return false_list;
			}
		};

	}])

	.factory('Alert',  ['$timeout',function($timeout) {

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
				}, 5000);

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

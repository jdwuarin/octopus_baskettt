angular.module('App.controllers').controller('BasketsCreateController',
	['$rootScope','$scope','Preference','Basket', 'Product', 'User','Tesco','Alert','$location','$anchorScroll', '$window', '$analytics','$modal', '$timeout','Cart',
	function($rootScope, $scope, Preference, Basket, Product, User, Tesco, Alert,$location,$anchorScroll,$window,$analytics,$modal,$timeout, Cart) {

		$scope.searchResults = [];
		$scope.cart = Cart.init();
		$scope.newBasketName = "";
		$scope.basketNameList = [];
		$scope.cartTotal = 0;
		$scope.searchPage = 0;
		$scope.searchAll = [];


		var itemsPerPage = 8;

		$scope.searchPageTotal = function(){
			return Math.floor($scope.searchAll.length / itemsPerPage) - 1;
		};

		var getSearchPage = function(page){
			if($scope.searchAll.length > 0 && page >= 0){
				var arr = $scope.searchAll.slice(itemsPerPage * page, (page + 1) * itemsPerPage - 1);
				return arr;
			}
		};

		$scope.searchProducts = function(query){
			Product.search(query)
			.then(function(res){
				$scope.searchAll = res;
				$scope.searchResults = getSearchPage(0);
			});
		};

		$scope.getNextSearch = function() {
			if($scope.searchPage >= $scope.searchPageTotal()) return;
			$scope.searchPage += 1;

			var newSearch = getSearchPage($scope.searchPage);
			if(newSearch.length > 0) $scope.searchResults = newSearch;
		};

		$scope.getPreviousSearch = function() {
			if($scope.searchPage <= 0) return;

			$scope.searchPage -= 1;
			var newSearch = getSearchPage($scope.searchPage);
			if(newSearch.length > 0) $scope.searchResults = newSearch;
		};

		$scope.autoComplete = function(query) {
			$scope.autocompleteResults = Product.autocomplete(query);
		};

		$rootScope.$on('searchEnter', function(e, query){
			$scope.searchProducts(query);
		});

		$scope.addProduct = function(newProduct) {
			$scope.cart = Cart.add(newProduct);
		};

		$scope.removeProduct = function(product) {
			$scope.cart = Cart.remove(product);
		};

		$scope.addBasket = function() {
			$scope.cart = Cart.addBasket($scope.newBasketName);
		};

		$scope.$watch('cart', function(newValue) {
			if(angular.isUndefined(newValue)){return;}

			$scope.cartTotal = Cart.computeTotal();
		}, true); //deep watching

		$scope.transferBasket = function(){

			var allProducts = Cart.getProducts();
			console.log('allProducts', allProducts);
			// When you open a form it will close the search
			if(allProducts && allProducts.length === 0){
				Alert.add('You need to add products to your basket to checkout.', 'info');
			}else {
				var modalInstance = $modal.open({
				templateUrl: 'static/app/partials/_modal.html',
				controller: 'ModalCtrl',
				resolve: {
					products: function () {
						return Cart.getProducts();
					}
				}
				});
			}

		};

		$scope.createBasket = function(){
			var createBasketParams = {};
			createBasketParams.name = 'Basket';

			createBasketParams.product_dict = Cart.getProducts()
				.map(function(p){
					return {
						query_term: 'test',
						quantity: p.quantity,
						id: p.id
					};
			});

			if(createBasketParams.product_dict.length === 0){
				return Alert.add("You didn't add any product.","danger");
			}

			createBasketParams.is_browsable = true;
			createBasketParams.is_public = true;

			Basket.create(createBasketParams).then(function(res){
				if(res.status === 201){
					return Alert.add("New basket created","success");
				}
			});

		};

		// Initialize variables for the frontend
	// 	var preferenceList = Preference.getAll();

	// 	$scope.tesco_response = {};
	// 	$scope.user = {};
	// 	$scope.tescoCredential = {};
	// 	$scope.search_result = {};
	// 	$scope.autocompleteResult = [];
	// 	$scope.basketMessage = User.isLoggedIn();

	// 	$scope.oldBasket = Basket.getLocal();
	// 	var hasOldBasket = $scope.oldBasket.length !== 0;

	// 	if(hasOldBasket){
	// 		$scope.products = $scope.oldBasket;
	// 		$scope.basketMessage = false;
	// 		$window.scrollTo(0,0);
	// 	}

	// 	$scope.getBasket = function() {

	// 		// First action on the page -> load the recommended basket
	// 		if(!Preference.isNotValid(preferenceList) || User.isLoggedIn()){
	// 			$scope.loading = true;
	// 			$scope.basketMessage = false;
	// 			Basket.post(preferenceList, function(res){
	// 				$scope.loading = false;
	// 				$window.scrollTo(0,0);

	// 				if(res.success === false){
	// 					Alert.add("We couldn't create your basket.","danger");
	// 				} else {
	// 					// Flush temp basket
	// 					Basket.addLocal([]);
	// 					Basket.addOldRecommendation(res.recommended_basket);
	// 					if(!User.isLoggedIn()) {
	// 						Basket.setUserSettingsKey(res.user_settings_hash);
	// 					} else {
	// 						Basket.setRecommendedBasketId(res.recommended_basket_id);
	// 					}

	// 					$scope.products = Product.formatUI(res.recommended_basket);
	// 					Basket.addLocal($scope.products);
	// 				}

	// 			});
	// 		} else {
	// 			Alert.add("Tell us what you like and we'll take care of your basket.","info");
	// 			User.redirect("/start");
	// 		}
	// 	};

	// 	if(!User.isLoggedIn() && !hasOldBasket) {
	// 		$scope.getBasket();
	// 	}

	// 	$scope.clearResult = function(){
	// 		$scope.search_result = {};
	// 	};

	// 	// GET search
	// 	$scope.searchProducts = function(query){
	// 		if(query) {
	// 			Product.search(query, function(res){ // success
	// 					$scope.search_result = Product.getQuantity(res, $scope.products);
	// 					$window.onclick = function (event) {
	// 						closeSearchWhenClickingElsewhere(event);
	// 					};
	// 				},function(res){ // error
	// 					Alert.add("Could not find this product","danger");
	// 					$scope.search_result = {};
	// 				});
	// 		} else {
	// 			$scope.search_result = {};
	// 		}
	// 	};


	// 	$scope.autoComplete = function(query) {
	// 		if(typeof query === "undefined" || query.length === 0){ return [];}

	// 		Product.autocomplete(query, function(res){
	// 			$scope.autocompleteResult = [];

	// 			angular.forEach(res.data, function(item){
	// 				$scope.autocompleteResult.push(item.name);
	// 			});
	// 		});
	// 	};

	// 	// Forces user to loggin if he wants to transfer his basket
	// 	$scope.transferBasket = function(){
	// 		// When you open a form it will close the search
	// 		$scope.clearResult();
	// 		if(!$scope.products){
	// 			Alert.add("You need to add products to your basket to checkout.", "info");
	// 		} else {
	// 			var modalInstance = $modal.open({
	// 			templateUrl: 'static/app/partials/_modal.html',
	// 			controller: 'ModalCtrl',
	// 			resolve: {
	// 				products: function () {
	// 					return $scope.products;
	// 				}
	// 			}
	// 			});
	// 		}

	// 	};

	// 	$scope.addProduct = function(new_product) {
	// 		if(new_product.quantity < 50){
	// 			Product.add($scope.products, new_product);
	// 			Basket.addLocal($scope.products);
	// 		}
	// 	};

	// 	$scope.removeProduct = function(product) {
	// 		Product.remove($scope.products, product);
	// 		Basket.addLocal($scope.products);
	// 	};

	// 	$scope.getTotal = function(val1,val2) {
	// 		return (parseFloat(val1.replace("GBP","")) * parseFloat(val2)).toFixed(2);
	// 	};

	// 	$scope.basketTotal = function() {
	// 		return Product.getTotal($scope.products);
	// 	};

	// 	// When you remove a product from the directive you need to update the scope
	// 	$rootScope.$on('deleteProduct', function(event, item){
	// 		$scope.products = Product.delete($scope.products, item);
	// 		$scope.$apply();
	// 		Basket.addLocal($scope.products);
	// 	});

	// 	$rootScope.$on('searchEnter', function(event, query){
	// 		console.log(query);
	// 		$scope.searchProducts(query);
	// 	});

	// 	var closeSearchWhenClickingElsewhere = function(event){

	// 		var clickedElement = event.target,
	// 		parents = angular.element(clickedElement).parents(),
	// 		clickedOnTheSearchPanel = false;

	// 		// checks if the parents of the div is one of the following string
	// 		for (var i = parents.length - 1; i >= 0; i--) {
	// 			if(parents[i].className.indexOf("product-search-result") != -1 ||
	// 				parents[i].className.indexOf("search-bar") != -1){
	// 				clickedOnTheSearchPanel = true;
	// 		}
	// 	}

	// 	if(!clickedOnTheSearchPanel){
	// 		$scope.clearResult();
	// 		$scope.$digest();
	// 	}
	// };

}]);

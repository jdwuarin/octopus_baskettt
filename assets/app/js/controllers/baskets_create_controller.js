angular.module('App.controllers').controller('BasketsCreateController',
	['$rootScope','$scope','Preference','Basket', 'Product', 'User','Tesco','Alert','$location','$anchorScroll', '$window', '$analytics','$modal', '$timeout','Cart',
	function($rootScope, $scope, Preference, Basket, Product, User, Tesco, Alert,$location,$anchorScroll,$window,$analytics,$modal,$timeout, Cart) {

		$scope.searchResults = [];
		$scope.cart = Cart.init();
		$scope.newBasketName = "";
		$scope.basketNameList = [];
		$scope.cartTotal = 0;

		$scope.searchProducts = function(query){
			$scope.searchResults = Product.search(query);
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

		$scope.addBasket = function() {
			$scope.cart = Cart.addBasket($scope.newBasketName);
		};


		$scope.$watch('cart', function(newValue, oldValue) {
			if(angular.isUndefined(newValue)){return;}

			console.log("change", newValue);
			$scope.cartTotal = Cart.computeTotal();
		}, true); //deep watching


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

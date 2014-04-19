angular.module('App.filters').filter('price', function() {
	return function(price) {
		return price.replace("GBP","");
	};
});

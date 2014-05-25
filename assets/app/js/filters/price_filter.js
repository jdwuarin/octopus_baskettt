angular.module('App.filters').filter('price', function() {
	return function(price) {
		if(price === 0 || typeof price === 'undefined'){return '';}

		return '£'+ parseFloat(price.replace("GBP","")).toFixed(2);
	};
});

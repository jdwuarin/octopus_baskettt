angular.module('App.filters').filter('price', function() {
	return function(price) {
		console.log('price filter ', price);
		if(price === 0 || typeof price === 'undefined'){return '';}

		return '£'+ parseFloat(price.replace("GBP","")).toFixed(2);
	};
});

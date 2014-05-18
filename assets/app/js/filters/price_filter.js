angular.module('App.filters').filter('price', function() {
	return function(price) {
		if(typeof price === 'undefined') return '';
		return '£'+ price.replace("GBP","");
	};
});

'use strict';

/* Filters */

angular.module('App.filters', [])
.filter('price', function() {
	return function(price) {
		return price.replace("GBP","");
	};
})

// get the large version of tesco's images
.filter('imglarge', function() {
	return function(url) {
		return url.replace("90x90.jpg","225x225.jpg");
	};
});

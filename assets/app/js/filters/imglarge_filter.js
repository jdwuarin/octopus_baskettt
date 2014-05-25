angular.module('App.filters').filter('imglarge', function() {
	return function(url) {
		return url.replace("90x90.jpg","225x225.jpg");
	};
});


'use strict';

/* Filters */

angular.module('App.filters', [])
.filter('price', function() {
	return function(price) {
		return price.replace("GBP","");
	};
})
.filter('orderObjectBy', function() {
  return function(items, field, reverse) {
    var filtered = [];
    angular.forEach(items, function(item) {
      filtered.push(item);
    });
    filtered.sort(function (a, b) {
      return (a[field] > b[field]);
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
})
// get the large version of tesco's images
.filter('imglarge', function() {
	return function(url) {
		return url.replace("90x90.jpg","225x225.jpg");
	};
});

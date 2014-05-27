angular.module('App.filters').filter('link', function() {
    return function(basket) {

        return 'baskettt.co/#/baskets/' + basket.hash;
    };
});

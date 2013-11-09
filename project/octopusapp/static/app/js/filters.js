'use strict';

/* Filters */

angular.module('App.filters', []).
filter('filteredrecipes', [function() {
	return function(recipes,diets){
		var result = recipes.slice();// copy array
		var recipe; 

		angular.forEach(diets, function(value, key) { //Checks if the keyword is in the title
			if(value) {
				for(var index = 0; index < result.length; index++) {
					recipe = result[index];
					if(recipe.title.indexOf(key) == -1) {
						result.splice(index--,1);
					}
				}
			}
		});
		return result;
	};
}]);
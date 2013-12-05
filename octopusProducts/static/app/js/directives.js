'use strict';

/* Directives */


angular.module('App.directives', [])

	// When you click on the DOM a the .selected class is injected
	.directive('click', ['selectedRecipes',function(selectedRecipes) {
		return function(scope, element, attrs) {
			element.bind("click", function() {
				scope.boolChangeClass = !scope.boolChangeClass;
				selectedRecipes.setObjects(scope.product);
				scope.$parent.cart = selectedRecipes.getObjects();
				scope.$apply();
			});
		};
	}]);
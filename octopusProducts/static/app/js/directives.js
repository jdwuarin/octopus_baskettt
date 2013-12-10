'use strict';

/* Directives */


angular.module('App.directives', [])

	// When you click on the DOM a the .selected class is injected
	.directive('click', ['Preference',function(Preference) {
		return function(scope, element, attrs) {

			//Initialize the status
			var selected_preference = Preference.getCuisine();

			var selected = selected_preference.some(function(el){
				return scope.cuisine.name === el;
			});

			scope.selectedStatus = selected;
			
			element.bind("click", function() {

				scope.selectedStatus = !scope.selectedStatus;
				Preference.setCuisine(scope);
				scope.$apply();
			});
		};
	}])


	.directive('remove', [function() {

		return {
			link: function (scope, element, attrs) {
				scope.$on('resetSelection', function() {
					scope.selectedStatus = false;
				});

				element.bind("click", function() {
					scope.selectedStatus = !scope.selectedStatus;
					scope.$apply();
				});
			},
			template: '<i class="glyphicon glyphicon-remove"></i>',
			transclude: true
		};
		
	}]);

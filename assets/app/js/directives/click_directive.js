angular.module('App.directives').directive('click', ['Preference',function(Preference) {
		return function(scope, element, attrs) {

			//Initialize the status
			var preferences = Preference.getAll().cuisine;

			var selected = preferences.some(function(el){
				return scope.cuisine.name === el;
			});

			scope.selectedStatus = selected;

			element.bind("click", function() {
				scope.selectedStatus = !scope.selectedStatus;
				Preference.setCuisine(scope.cuisine.name, scope.selectedStatus);
				scope.$apply();
			});
		};
	}]);



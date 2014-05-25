angular.module('App.directives').directive('onboardPeople',
	['$rootScope',
	function($rootScope){
		return {
			link: function(scope, element, attrs) {
				element.bind("click", function(event){
					$rootScope.$emit('peoplePosition', parseInt(attrs.position,10));
				});
			}
		};
	}]);


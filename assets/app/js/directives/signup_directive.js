angular.module('App.directives').directive('signup',[function() {
		return {
			link: function (scope, element, attrs) {
				scope.isVisible = false;
				scope.toggleForm = function(value){
					scope.isVisible = value;
				};
			},
			restrict: 'E',
			templateUrl: 'static/app/partials/_sign_up.html'
		};
	}]);



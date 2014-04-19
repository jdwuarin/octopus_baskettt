angular.module('App.directives').directive('remove', ['$rootScope',function($rootScope) {

		return {
			link: function (scope, element, attrs) {
				element.bind("click", function() {
					$rootScope.$emit('deleteProduct', scope.product);
				});
			},
			template: '<i class="glyphicon glyphicon-remove"></i>',
			transclude: true
		};

	}]);

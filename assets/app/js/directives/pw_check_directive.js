angular.module('App.directives').directive('pwCheck',
	[function () {
	return {
		require: 'ngModel',
		link: function (scope, element, attrs, ctrl) {
			var firstPassword = '#' + attrs.pwCheck;
			element.add(firstPassword).on('keyup', function () {
				scope.$apply(function () {
					var v = element.val()===$(firstPassword).val();
					ctrl.$setValidity('pwmatch', v);
				});
			});
		}
	};

	}]);

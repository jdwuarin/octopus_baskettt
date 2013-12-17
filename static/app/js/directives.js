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

	.directive('signup',[function() {
		return {
			link: function (scope, element, attrs) {
				scope.isVisible = false;
				scope.toggleForm = function(value){
					console.log("313");
					scope.isVisible = value;
				};
			},
			restrict: 'E',
			templateUrl: 'static/app/partials/_sign_up.html'
		};
	}])

	.directive('tesco',[function() {
		return {
			link: function (scope, element, attrs) {
				scope.tescoIsVisible = false;
				scope.toggleTescoForm = function(value){
					scope.tescoIsVisible = value;
				};
			},
			restrict: 'E',
			templateUrl: 'static/app/partials/_tesco.html'
		};
	}])

	.directive('navbar',['$rootScope', 'User', function($rootScope, User) {

		return {
			link: function (scope, element, attrs) {

				$rootScope.$on('UserSignedUp', function(){
					User.requestLoggedIn(function(res){
						if(res.success){
							User.setLoggedIn(true);
							scope.userIsLoggedIn();
							$rootScope.$emit('CloseSignUpForm');
						}
					});
				});

				scope.userIsLoggedIn = function(){
					// Defined as a function to force the execution after a redirection
					return User.isLoggedIn();
				};

				scope.logout = function(){
					User.logout(function(data){
						User.setLoggedIn(false);
						// This callback is only called when return success
						User.redirect("/");
					});
				};
			},
			restrict: 'E',
			templateUrl: 'static/app/partials/_nav_bar.html'
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

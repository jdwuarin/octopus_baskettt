'use strict';

/* Directives */


angular.module('App.directives', [])

	.directive('basket', ['$rootScope', function($rootScope){
		return {
			templateUrl: 'static/app/partials/_basket_detail.html',
			restrict: 'E',
			link: function(scope) {

				scope.showBasket = false;

				$rootScope.$on('showBasketDetails', function(){
					scope.showBasket = true;
				});
			}
		};
	}])

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

	.directive('remove', ['$rootScope',function($rootScope) {

		return {
			link: function (scope, element, attrs) {
				element.bind("click", function() {
					$rootScope.$emit('removeProduct', scope.$index);
				});
			},
			template: '<i class="glyphicon glyphicon-remove"></i>',
			transclude: true
		};

	}]);

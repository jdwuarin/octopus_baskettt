'use strict';

/* Directives */

angular.module('App.directives', [])

	.directive('scrollTo',[function(){
		return function(scope, element, attrs){
			element.bind("click", function(event){
				var $selector = $(attrs.scrollTo);
				if($selector.length){
					$("html, body").animate({
						// 65 because it looks about right
						scrollTop : $selector[0].offsetTop - 65
					}, 1000);
				}
			});
		};
	}])

	.directive('onboardPeople', ['$rootScope', function($rootScope){
		return {
			link: function(scope, element, attrs) {
				element.bind("click", function(event){
					$rootScope.$emit('peoplePosition', parseInt(attrs.position,10));
				});
			}
		};
	}])

	.directive('ngEsc', [function(){
		return function(scope, element, attrs) {
			element.bind("keydown keypress", function(event) {
				if(event.which === 27) {
					scope.$apply(function (){
						scope.$eval(attrs.ngEsc);
					});

					event.preventDefault();
				}
			});
		};
	}])

	// When you click on the DOM a the .selected class is injected
	.directive('click', ['Preference',function(Preference) {
		return function(scope, element, attrs) {

			//Initialize the status
			var preferences = Preference.getAll().cuisine;

			var selected = preferences.some(function(el){
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

	.directive('navbar',['$rootScope', 'User', '$location', function($rootScope, User, $location) {

		return {
			link: function (scope, element, attrs) {

				$rootScope.$on('UserSignedUp', function(){
					User.requestLoggedIn(function(res){
						if(res.success){
							User.setLoggedIn(true);
							scope.userIsLoggedIn();
						}
					});
				});

				var fs = false;

				scope.fullscreen = function (){
					fs = $location.path().indexOf('onboarding') !=-1;
					if(fs){
						angular.element('body').css('padding-top','0px');
					}
					return fs;
				};

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
					$rootScope.$emit('deleteProduct', scope.product);
				});
			},
			template: '<i class="glyphicon glyphicon-remove"></i>',
			transclude: true
		};

	}]);

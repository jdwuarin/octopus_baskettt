angular.module('App.directives').directive('navbar',['$rootScope', 'User', '$location','localStorage', function($rootScope, User, $location, localStorage) {

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
						localStorage.flush();
						// This callback is only called when return success
						User.redirect("/");
					});
				};
			},
			restrict: 'E',
			templateUrl: 'static/app/partials/_nav_bar.html'
		};
	}]);

angular.module('App.controllers').controller('HomeController',
	['$scope', '$sanitize', 'User','$analytics','$anchorScroll','$location',
	function($scope, $sanitize, User, $analytics, $anchorScroll,$location){

		$scope.betaSuccess = false;

		$scope.scrollTo = function(id) {
			$location.hash(id);
			$anchorScroll();
		};

		$scope.registerForBeta = function(){

			if($scope.betaForm.$valid){

				User.registerBeta($scope.email, function(data){
					// This callback is only called when return success
					$analytics.eventTrack('RegisterToBeta',
						{ category: 'Onboarding'});
					$scope.betaSuccess = true;
				});
			}
		};

		// Twitter share button
		!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');

}]);


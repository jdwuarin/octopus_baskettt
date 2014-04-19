angular.module('App.controllers').controller('OnboardingController', ['$scope', '$routeParams', 'Preference','Alert','$location','$anchorScroll','$window', '$rootScope', 'Basket', function($scope, $routeParams, Preference, Alert, $location, $anchorScroll, $window, $rootScope, Basket) {

	$scope.cuisines = [
	{ "name": "Italian", "image": "italy.png"},
	{ "name": "Chinese", "image": "china.png"},
	{ "name": "Indian", "image": "india.png"},
	{ "name": "Spanish", "image": "spain.png"},
	{ "name": "Thai",  "image": "thai.png"},
	{ "name": "French",  "image": "france.png"}
	];

	$scope.preference = Preference.getAll();
	$scope.number = 8;
	$scope.peopleIndex = 1;
	$scope.preference.days = 7;
	$scope.cookingValue = 50;

	$window.scrollTo(0,0);

	Basket.clearLocal();

	// Generate empty array for ng-repeat to display the people icons
	$scope.getNumber = function(num) {
		return new Array(num);
	};

	$scope.addDays = function(){
		if($scope.preference.days < 10) {
			$scope.preference.days++;
		}
	};

	$scope.removeDays = function(){
		if($scope.preference.days !==1) {
			$scope.preference.days--;
		}
	};

	$scope.generateBasket = function() {
		$scope.preference.people = $scope.peopleIndex+1;
		$scope.preference.price_sensitivity = parseInt($scope.cookingValue, 10) / 100;

		if(Preference.isNotValid($scope.preference)) {
			Alert.add("It looks like you didn't select all of your preferences.","danger");
			// Scroll to top
			$location.hash('wrap');
			$anchorScroll();
		}
		else {
			Preference.setParameters($scope.preference);
			$location.path("/basket");
		}
	};


	$rootScope.$on('peoplePosition', function(event, selectedIndex){
		$scope.peopleIndex = selectedIndex;
		$scope.$digest();
	});

	// JQuery logic in the controller because I don't have access to the
	// ui-slider directive - ugly but does the work
	angular.element('.slider-bar').bind('mouseup', function(){
		$scope.preference.price_sensitivity = $scope.cookingValue;
	});

}]);

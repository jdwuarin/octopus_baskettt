describe('OnboardingController', function(){

	//Mocks
	var windowMock, httpBackend, _Preference, sharedMock;

	//Controller
	var ctrl;

	//Scope
	var ctrlScope;

	//Data
	var cuisines = [
		{ "name": "Italian", "image": "italian.png"},
		{ "name": "Chinese", "image": "chinese.png"},
		{ "name": "Indian", "image": "indian.png"},
		{ "name": "Spanish", "image": "spanish.png"},
		{ "name": "Thai",  "image": "thai.png"},
		{ "name": "French",  "image": "french.png"}
	];

	//Loading shopping module
	beforeEach(function () {
		module("App");
	});

	beforeEach(inject(function ($rootScope, $httpBackend, $controller, Preference) {

		// New scope
		ctrlScope = $rootScope.$new();
		_Preference = Preference;

		spyOn(Preference, 'getAll').andCallThrough();

		//Creating controller with assigning mocks instead of actual services
		ctrl = $controller('OnboardingController', { $scope: ctrlScope, Preference: _Preference});
	}));


	it("Should get the Preferences from a previous session", function(){
		expect(_Preference.getAll()).not.toBe(null);
	});
});

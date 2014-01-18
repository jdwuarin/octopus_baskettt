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

	var mockUserPreferences = {"cuisine":["Italian"],"people":"2", "budget":"100","days":"3" };
	var mockCuisineName = {"name":"Italian"};

	//Loading shopping module
	beforeEach(function () {
		module("App");
	});

	beforeEach(inject(function ($rootScope, $httpBackend, $controller, Preference, localStorageService) {

		// Create mock
		ctrlScope = $rootScope.$new();
		_Preference = Preference;
		_localStorageService = localStorageService;

		spyOn(Preference, 'getAll').andCallThrough();

		//Creating controller with assigning mocks instead of actual services
		ctrl = $controller('OnboardingController', { $scope: ctrlScope, Preference: _Preference, localStorageService: _localStorageService});
	}));

	it("Should get the Preferences from a previous session", function(){
		expect(_Preference.getAll()).not.toBe(null);
	});

	describe("Selected favorite cuisine", function() {

		beforeEach(function(){
			ctrlScope.cuisine = mockCuisineName;
			ctrlScope.selectedStatus = true;
			_Preference.setCuisine(ctrlScope);
		});

		// Onboarding step 1
		it("Should save the cuisine preference of a user", function(){
			expect(_Preference.getAll().cuisine['0']).toBe(mockCuisineName.name);
		});
			// Onboarding step 2
		it("Should save the cuisine, people, budget and days preferences of a user", function(){
			ctrlScope.preference = mockUserPreferences;
			ctrlScope.saveData();

			var fetchedPref = _Preference.getAll();

			expect(fetchedPref.cuisine["0"]).toBe(mockUserPreferences.cuisine["0"]);
			expect(fetchedPref.days).toBe(mockUserPreferences.days);
			expect(fetchedPref.people).toBe(mockUserPreferences.people);
			expect(fetchedPref.budget).toBe(mockUserPreferences.budget);
		});
	});

});

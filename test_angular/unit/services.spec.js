// Service: Preference

describe('Preference', function(){

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

	var mockUserPreferences = {"cuisine":["Thai","French"],"price_sensitivity":0.5, "budget":500, "people":4, "days":7};
	var mockCuisineName = {"name":"Italian"};

	//Loading App module
	beforeEach(function () {
		module("App");
	});

	beforeEach(inject(function (Preference) {

		// Create mock
		_Preference = Preference;
		spyOn(Preference, 'getAll').andCallThrough();

	}));

	it("Should get the Preferences from a previous session", function(){
		expect(_Preference.getAll()).not.toBe(null);
	});


	it("Should save the cuisine, people, price_sensitivity and days preferences of a user", function(){

		_Preference.setParameters(mockUserPreferences);
		var fetchedPref = _Preference.getAll();

		expect(fetchedPref.cuisine["0"]).toBe(mockUserPreferences.cuisine["0"]);
		expect(fetchedPref.days).toBe(mockUserPreferences.days);
		expect(fetchedPref.people).toBe(mockUserPreferences.people);
		expect(fetchedPref.price_sensitivity).toBe(mockUserPreferences.price_sensitivity);
	});

	it("Should check if the preferences is valid", function(){
		expect(_Preference.isNotValid(mockUserPreferences)).toBe(false);
	});

	it("Should check if the preferences is not valid", function(){
		mockUserPreferences["days"] = -1;
		mockUserPreferences["people"] = -1;
		mockUserPreferences["price_sensitivity"] = 100;
		expect(_Preference.isNotValid(mockUserPreferences)).toBe(true);
	});

});
